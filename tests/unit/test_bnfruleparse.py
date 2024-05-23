import pytest


from plcc.spec.bnfrule import BnfRule
from plcc.spec.bnfparser import BnfParser
from plcc.spec.line import Line


@pytest.fixture
def bnfParser():
    return BnfParser()


def toLine(string):
    return Line(
        path='',
        number=1,
        string=string,
        isInBlock=False
    )


def test_standard(bnfParser):
    bnfRule = bnfParser.parseBnfRule(toLine('<one> ::= TWO <three> <FOUR> <five>hi <six>:by <SEVEN>:go # comment'))
    assert bnfRule.lhs.name == 'one'
    assert not bnfRule.lhs.alt
    assert bnfRule.op == '::='
    assert len(bnfRule.tnts) == 6
    assert bnfRule.tnts[0].name == 'TWO'


def test_repeating(bnfParser):
    bnfRule = bnfParser.parseBnfRule(toLine('<one>:One **= <two> +THREE # comment'))
    assert bnfRule.op == '**='
    assert bnfRule.sep.name == 'THREE'


def test_missing_op(bnfParser):
    with pytest.raises(BnfParser.MissingDefinitionOperator):
        bnfParser.parseBnfRule(toLine('<one>:One *= <two> +THREE # comment'))


def test_invalid_nonterminal(bnfParser):
    with pytest.raises(BnfParser.InvalidNonterminal):
        bnfParser.parseBnfRule(toLine('<ONE>:One ::= <two> THREE'))


def test_unrecognized_rhs(bnfParser):
    with pytest.raises(BnfParser.ExtraContent):
        bnfParser.parseBnfRule(toLine('<one> ::= <two> THREE @32'))
