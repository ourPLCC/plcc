import pytest


from plcc.specfile.bnfparse import BnfRuleParser, NonterminalParser, RhsParser, BnfRule


def test_standard():
    bnfRule = BnfRuleParser().parse('<one> ::= TWO <three> <FOUR> <five>hi <six>:by <SEVEN>:go # comment')
    assert bnfRule.lhs.name == 'one'
    assert not bnfRule.lhs.alt
    assert bnfRule.op == '::='
    assert len(bnfRule.tnts) == 6
    assert bnfRule.tnts[0].name == 'TWO'

def test_repeating():
    BnfRuleParser().parse('<one>:One **= <two> +THREE # comment')

def test_missing_op():
    with pytest.raises(BnfRuleParser.MissingDefinition):
        BnfRuleParser().parse('<one>:One *= <two> +THREE # comment')

def test_separator_with_standard():
    with pytest.raises(BnfRuleParser.IllegalSeparator):
        BnfRuleParser().parse('<one>:One ::= <two> +THREE # comment')

def test_invalid_nonterminal():
    with pytest.raises(NonterminalParser.InvalidNonterminalName):
        BnfRuleParser().parse('<ONE>:One ::= <two> THREE')

def test_unrecognized_rhs():
    with pytest.raises(RhsParser.Unrecognized):
        BnfRuleParser().parse('<one> ::= <two> THREE @32')
