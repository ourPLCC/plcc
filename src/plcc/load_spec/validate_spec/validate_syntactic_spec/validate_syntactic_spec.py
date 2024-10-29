from ...parse_spec.parse_syntactic_spec import (
    SyntacticSpec,
    SyntacticRule,
)
from ...parse_spec.parse_lexical_spec import LexicalSpec
from .validate_lhs import validate_lhs
from .validate_rhs import validate_rhs


def validate_syntactic_spec(syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec):
    return SyntacticValidator(syntacticSpec, lexicalSpec).validate()


class SyntacticValidator:
    lexicalSpec: LexicalSpec
    syntacticSpec: SyntacticSpec
    rule: SyntacticRule

    def __init__(self, syntacticSpec: SyntacticSpec, lexicalSpec: LexicalSpec):
        self.syntacticSpec = syntacticSpec
        self.lexicalSpec = lexicalSpec
        self.errorList = []
        self.nonTerminals = set()

    def validate(self) -> list:
        if not self.syntacticSpec:
            return self.errorList
        self._validateLhs()
        return self.errorList

    def _validateLhs(self):
        lhs_error_list, non_terminal_set = validate_lhs(self.syntacticSpec)
        if lhs_error_list:
            self.errorList = lhs_error_list
        self.nonTerminals = non_terminal_set

    def _validateRhs(self):
        _ = validate_rhs(self.syntacticSpec,
                         self.lexicalSpec, self.nonTerminals)
