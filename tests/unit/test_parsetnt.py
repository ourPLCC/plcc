import pytest


from plcc.spec.bnfparser import BnfParser
from plcc.spec.bnfparser import MatchScanner
from plcc.spec.bnfrule import Tnt
from plcc.spec.bnfrule import TntType


def test_invalid_tnt():
    with pytest.raises(BnfParser.InvalidTnt):
        BnfParser().parseTnt(MatchScanner('-'))


def test_terminal():
    tnt = BnfParser().parseTnt(MatchScanner('HI'))
    assert tnt == Tnt(type=TntType.TERMINAL, name='HI', alt='', capture=False)



def test_captured_terminal():
    tnt = BnfParser().parseTnt(MatchScanner('<HI>'))
    assert tnt == Tnt(type=TntType.TERMINAL, name='HI', alt='', capture=True)



def test_captured_terminal_with_alt():
    tnt = BnfParser().parseTnt(MatchScanner('<HI>greet'))
    assert tnt == Tnt(type=TntType.TERMINAL, name='HI', alt='greet', capture=True)



def test_captured_terminal_with_alt_colon():
    tnt = BnfParser().parseTnt(MatchScanner('<HI>:greet'))
    assert tnt == Tnt(type=TntType.TERMINAL, name='HI', alt='greet', capture=True)



def test_captured_nonterminal():
    tnt = BnfParser().parseTnt(MatchScanner('<hi>'))
    assert tnt == Tnt(type=TntType.NONTERMINAL, name='hi', alt='', capture=True)



def test_captured_nonterminal_with_alt():
    tnt = BnfParser().parseTnt(MatchScanner('<hi>greet'))
    assert tnt == Tnt(type=TntType.NONTERMINAL, name='hi', alt='greet', capture=True)



def test_captured_nonterminal_with_alt_colon():
    tnt = BnfParser().parseTnt(MatchScanner('<hi>:greet'))
    assert tnt == Tnt(type=TntType.NONTERMINAL, name='hi', alt='greet', capture=True)



def test_captured_nonterminal_with_remainder():
    tnt = BnfParser().parseTnt(MatchScanner('<hi>:greet more stuff'))
    assert tnt == Tnt(type=TntType.NONTERMINAL, name='hi', alt='greet', capture=True)
