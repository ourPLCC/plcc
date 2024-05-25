import pytest


import plcc.spec.bnfparser as bp
from plcc.spec.bnfrule import BnfRule
from plcc.spec.line import Line


@pytest.fixture
def bnfParser():
    return bp.BnfParser()


def toLine(string):
    return Line(
        path='',
        number=1,
        string=string,
        isInCodeBlock=False
    )


def test_standard(bnfParser):
    bnfRule = bnfParser.parseBnfRule(toLine('<one> ::= TWO <three> <FOUR> <five>hi <six>:by <SEVEN>:go # comment'))
    assert bnfRule.leftHandSymbol.name == 'one'
    assert not bnfRule.leftHandSymbol.alt
    assert not bnfRule.isRepeating
    assert len(bnfRule.rightHandSymbols) == 6
    assert bnfRule.rightHandSymbols[0].name == 'TWO'


def test_repeating(bnfParser):
    bnfRule = bnfParser.parseBnfRule(toLine('<one>:One **= <two> +THREE # comment'))
    assert bnfRule.isRepeating
    assert bnfRule.separator.name == 'THREE'


def test_missing_op(bnfParser):
    assert_fails(bnfParser, '<one>:One *= <two> +THREE # comment', bp.MissingDefinitionOperator)


def test_invalid_nonterminal(bnfParser):
    assert_fails(bnfParser, '<ONE>:One ::= <two> THREE', bp.InvalidNonterminal)


def test_unrecognized_rhs(bnfParser):
    assert_fails(bnfParser, '<one> ::= <two> THREE @32', bp.ExtraContent)


def assert_fails(parser, string, exception):
    with pytest.raises(exception):
        parser.parseBnfRule(toLine(string))
