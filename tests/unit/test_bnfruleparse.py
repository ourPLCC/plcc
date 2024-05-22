import pytest


from plcc.specfile.bnfrule import BnfRule
from plcc.specfile.bnfparser import BnfParser


def test_standard():
    bnfRule = BnfParser().parseBnfRule('<one> ::= TWO <three> <FOUR> <five>hi <six>:by <SEVEN>:go # comment')
    assert bnfRule.lhs.name == 'one'
    assert not bnfRule.lhs.alt
    assert bnfRule.op == '::='
    assert len(bnfRule.tnts) == 6
    assert bnfRule.tnts[0].name == 'TWO'

def test_repeating():
    BnfParser().parseBnfRule('<one>:One **= <two> +THREE # comment')

def test_missing_op():
    with pytest.raises(BnfParser.MissingDefinitionOperator):
        BnfParser().parseBnfRule('<one>:One *= <two> +THREE # comment')

def test_separator_with_standard():
    with pytest.raises(BnfParser.StandardRuleCannotHaveSeparator):
        BnfParser().parseBnfRule('<one>:One ::= <two> +THREE # comment')

def test_invalid_nonterminal():
    with pytest.raises(BnfParser.InvalidNonterminal):
        BnfParser().parseBnfRule('<ONE>:One ::= <two> THREE')

def test_unrecognized_rhs():
    with pytest.raises(BnfParser.ExtraContent):
        BnfParser().parseBnfRule('<one> ::= <two> THREE @32')
