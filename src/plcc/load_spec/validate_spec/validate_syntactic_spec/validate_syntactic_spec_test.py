from pytest import raises, mark, fixture
from typing import List

from ...load_rough_spec.parse_lines import Line
from .validate_syntactic_spec import validate_syntactic_spec
from ...parse_spec.parse_syntactic_spec import (
    SyntacticRule,
    SyntacticSpec,
    Symbol,
    LhsNonTerminal,
    Terminal,
)
from .errors import (
    InvalidLhsNameError,
    InvalidLhsAltNameError,
    DuplicateLhsError,
)


def test_empty_no_errors():
    syntacticSpec = makeSyntacticSpec([])
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def test_None_no_errors():
    syntacticSpec = makeSyntacticSpec(None)
    errors = validate_syntactic_spec(syntacticSpec)
    assert len(errors) == 0


def test_valid_line_no_errors():
    valid_line = makeLine("<sentence> ::= WORD")
    errors = validate_syntactic_spec(
        [
            makeSyntacticRule(
                valid_line, makeLhsNonTerminal("sentence"), [makeTerminal("WORD")]
            )
        ]
    )
    assert len(errors) == 0


def test_distinct_resolved_name():
    line_answer = makeSyntacticRule(
        makeLine("<sentence>:Answer ::= VERB"),
        makeLhsNonTerminal("sentence", "Answer"),
        [makeTerminal("VERB")],
    )
    line_question = makeSyntacticRule(
        makeLine("<sentence>:Question ::= WORD"),
        makeLhsNonTerminal("sentence", "Question"),
        [makeTerminal("WORD")],
    )
    errors = validate_syntactic_spec([line_answer, line_question])
    assert len(errors) == 0


def test_valid_lhs_alt_name():
    valid_line = makeLine("<sentence>:Name_Version_1 ::= WORD")
    errors = validate_syntactic_spec(
        [
            makeSyntacticRule(
                valid_line,
                makeLhsNonTerminal("sentence", "Name_Version_1"),
                [makeTerminal("WORD")],
            )
        ]
    )
    assert len(errors) == 0


def test_number_lhs_terminal():
    invalid_nonterminal = makeLine("<1sentence> ::= WORD")
    spec = [
        makeSyntacticRule(
            invalid_nonterminal, makeLhsNonTerminal("1sentence"), [makeTerminal("WORD")]
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsNameFormatError(spec[0])


def test_capital_lhs_terminal():
    capital_lhs_name = makeLine("<Sentence> ::= WORD")
    spec = [
        makeSyntacticRule(
            capital_lhs_name, makeLhsNonTerminal("Sentence"), [makeTerminal("WORD")]
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsNameFormatError(spec[0])


def test_undercase_lhs_alt_name():
    invalid_alt_name = makeLine("<sentence>:name ::= WORD")
    spec = [
        makeSyntacticRule(
            invalid_alt_name,
            makeLhsNonTerminal("sentence", "name"),
            [makeTerminal("WORD")],
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsAltNameFormatError(spec[0])


def test_underscore_lhs_alt_name():
    invalid_alt_name = makeLine("<sentence>:_name ::= WORD")
    spec = [
        makeSyntacticRule(
            invalid_alt_name,
            makeLhsNonTerminal("sentence", "_name"),
            [makeTerminal("WORD")],
        )
    ]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidLhsAltNameFormatError(spec[0])


def test_duplicate_lhs_name():
    lhs_sentence = makeLhsNonTerminal("sentence")
    rule_1 = makeSyntacticRule(
        makeLine("<sentence> ::= VERB"),
        lhs_sentence,
        [makeTerminal("VERB")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence> ::= WORD"),
        lhs_sentence,
        [makeTerminal("WORD")],
    )
    spec = [rule_1, rule_2]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_duplicate_lhs_alt_name():
    rule_1 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= VERB"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("VERB")],
    )
    rule_2 = makeSyntacticRule(
        makeLine("<sentence>:Name ::= WORD"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("WORD")],
    )
    spec = [rule_1, rule_2]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def test_duplicate_resolved_name():
    alt_name = makeSyntacticRule(
        makeLine("<sentence>:Name ::= VERB"),
        makeLhsNonTerminal("sentence", "Name"),
        [makeTerminal("VERB")],
    )
    non_terminal_name = makeSyntacticRule(
        makeLine("<name> ::= WORD"),
        makeLhsNonTerminal("name"),
        [makeTerminal("WORD")],
    )
    spec = [alt_name, non_terminal_name]
    errors = validate_syntactic_spec(spec)
    assert len(errors) == 1
    assert errors[0] == makeDuplicateLhsError(spec[1])


def makeSyntacticSpec(ruleList=None):
    return SyntacticSpec(ruleList)


def makeSyntacticRule(line: Line, lhs: LhsNonTerminal, rhsList: List[Symbol]):
    return SyntacticRule(line, lhs, rhsList)


def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)


def makeLhsNonTerminal(name: str | None, altName: str | None = None):
    return LhsNonTerminal(name, altName)


def makeTerminal(name: str | None):
    return Terminal(name)


def makeInvalidLhsNameFormatError(rule):
    return InvalidLhsNameError(rule)


def makeInvalidLhsAltNameFormatError(rule):
    return InvalidLhsAltNameError(rule)


def makeDuplicateLhsError(rule):
    return DuplicateLhsError(rule)
