import pytest


from plcc.specfile.bnfparse import BnfParser, NonterminalParser, RhsParser


def test_standard():
    BnfParser().parse('<one> ::= TWO <three> <FOUR> <five>hi <six>:by <SEVEN>:go # comment')

def test_repeating():
    BnfParser().parse('<one>:One **= <two> +THREE # comment')

def test_missing_op():
    with pytest.raises(BnfParser.MissingDefinition):
        BnfParser().parse('<one>:One *= <two> +THREE # comment')

def test_separator_with_standard():
    with pytest.raises(BnfParser.IllegalSeparator):
        BnfParser().parse('<one>:One ::= <two> +THREE # comment')

def test_invalid_nonterminal():
    with pytest.raises(NonterminalParser.InvalidNonterminalName):
        BnfParser().parse('<ONE>:One ::= <two> THREE')

def test_unrecognized_rhs():
    with pytest.raises(RhsParser.Unrecognized):
        BnfParser().parse('<one> ::= <two> THREE @32')
