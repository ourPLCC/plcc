from dataclasses import dataclass
import re
from re import Match
from ..load_rough_spec.parse_lines import Line

@dataclass
class LexicalRule:
    line: Line
    isSkip: bool
    name: str
    pattern: str

@dataclass
class LexicalSpec:
    ruleList: [LexicalRule|Line]

def parse_lexical_spec(lines: list[Line]) -> LexicalSpec:
    return LexicalParser(lines).parseLexicalSpec()

class LexicalParser():
    def __init__(self, lines: [Line]):
        self.lines = lines
        self.patterns = {
            'skipToken' : re.compile(r'^skip\s+(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$'),
            'tokenToken' : re.compile(r'(?:^token\s+)?(?P<Name>\S+)\s+(?P<Pattern>((\'\S+\')|(\"\S+\")))\s*(?:#.*)*$')
        }
        self.spec = LexicalSpec([])

    def parseLexicalSpec(self) -> LexicalSpec:
        if not self.lines:
            return self.spec
        for line in self.lines:
            if self._isBlankOrComment(line):
                continue
            else:
                self._processLine(line)
        return self.spec

    def _processLine(self, line: Line):
            lineIsSkipToken, lineIsRegularToken = self._matchToken(line.string)
            if lineIsSkipToken or lineIsRegularToken:
                self.spec.ruleList.append(self._generateTokenRule(line, lineIsSkipToken, lineIsRegularToken))
            else:
                self.spec.ruleList.append(line)

    def _generateTokenRule(self, line: Line, lineIsSkipToken: Match[str], lineIsRegularToken: Match[str]) -> LexicalRule:
        if lineIsSkipToken:
            return self._generateSkipToken(line, lineIsSkipToken['Name'], lineIsSkipToken['Pattern'])
        elif lineIsRegularToken:
            return self._generateRegularToken(line, lineIsRegularToken['Name'], lineIsRegularToken['Pattern'])

    def _isBlankOrComment(self, line: Line) -> bool:
        return not line.string.strip() or line.string.strip().startswith("#")

    def _matchToken(self, lineStr: str) -> tuple[Match[str] | None, Match[str] | None]:
        isSkipToken = re.match(self.patterns['skipToken'], lineStr)
        isRegularToken = re.match(self.patterns['tokenToken'], lineStr)
        return isSkipToken, isRegularToken

    def _generateSkipToken(self, line: Line, name: str, pattern: str) -> LexicalRule:
        pattern = self._stripQuotes(pattern)
        newSkipRule = LexicalRule(line=line, isSkip=True, name=name, pattern=pattern)
        return newSkipRule

    def _generateRegularToken(self, line: Line, name: str, pattern: str) -> LexicalRule:
        pattern = self._stripQuotes(pattern)
        newTokenRule = LexicalRule(line=line, isSkip=False, name=name, pattern=pattern)
        return newTokenRule

    def _stripQuotes(self, pattern: str) -> str:
        pattern = pattern.strip('\'')
        pattern = pattern.strip('\"')
        return pattern
