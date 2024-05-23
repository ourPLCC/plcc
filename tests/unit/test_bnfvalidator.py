import pytest


from plcc.spec.reader import SpecReader
from plcc.spec.bnfspec import BnfSpec
from plcc.spec.bnfparser import BnfParser
from plcc.spec.bnfvalidator import BnfValidator


def toSpec(string):
    reader = SpecReader()
    parser = BnfParser()
    lines = reader.readLinesFromString(string)
    spec = parser.parseBnfSpec(lines)
    return spec


@pytest.fixture
def validator():
    return BnfValidator()


def test_detects_invalid_terminal_names(validator):
    spec = toSpec(
        '<hi> ::= MOm\n'
    )
    with pytest.raises(BnfValidator.InvalidTerminalName):
        validator.validate(spec)


def test_detects_duplicate_alts_in_LHS(validator):
    spec = toSpec(
        '<hi>One ::= <bye>\n'
        '<bye>One ::= MOM\n'
    )
    with pytest.raises(BnfValidator.DuplicateConcreteClassNameInLhs):
        validator.validate(spec)


def test_duplicate_LHS_nonterminals_must_have_an_alt(validator):
    spec = toSpec(
        '<hi> ::= DAD\n'
        '<hi>One ::= MOM\n'
    )
    with pytest.raises(BnfValidator.DuplicateLhsMustProvideConcreteClassName):
        validator.validate(spec)
