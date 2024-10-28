from dataclasses import dataclass
import re
from ...load_rough_spec.parse_lines import Line
from ...parse_spec.parse_lexical_spec import LexicalSpec, LexicalRule
from .lexical_errors import ValidationError, InvalidNameFormatError, DuplicateNameError, InvalidPatternError, InvalidRuleError

def validate_lexical_spec(lexicalSpec: LexicalSpec):
    return LexicalValidator(lexicalSpec).validate()

class LexicalValidator:
    def __init__(self, lexicalSpec: LexicalSpec):
        self.lexicalSpec = lexicalSpec
        self.errorList = []
        self.names = set()
        self.patterns = set()
        self.namePattern = re.compile(r'^[A-Z_][A-Z0-9_]*$')

    def validate(self) -> list:
        if self._isSpecEmpty():
            return self.errorList
        for rule in self.lexicalSpec.ruleList:
            self._handle(rule)
        return self.errorList

    def _isSpecEmpty(self):
        return not (self.lexicalSpec and self.lexicalSpec.ruleList)

    def _handle(self, rule: LexicalRule | Line):
        if isinstance(rule, LexicalRule):
            self._checkNameFormat(rule)
            self._checkDuplicateNames(rule)
            self._checkPatternFormat(rule)
        else:
            self._checkForLine(rule)

    def _checkNameFormat(self, rule: LexicalRule):
        if not self.namePattern.match(rule.name):
            self.errorList.append(InvalidNameFormatError(rule=rule))

    def _checkDuplicateNames(self, rule: LexicalRule):
        if rule.name in self.names:
            self.errorList.append(DuplicateNameError(rule=rule))
        else:
            self.names.add(rule.name)

    def _checkPatternFormat(self, rule: LexicalRule):
        if "\'" in rule.pattern or "\"" in rule.pattern or rule.pattern == '':
            self.errorList.append(InvalidPatternError(rule=rule))

    def _checkForLine(self, line: Line):
        self.errorList.append(InvalidRuleError(line=line))
