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
        '<hi> ::= MOm'
    )
    with pytest.raises(BnfValidator.InvalidTerminalName):
        validator.validate(spec)
