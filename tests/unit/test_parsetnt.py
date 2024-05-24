import pytest


from plcc.spec.bnfparser import BnfParser
from plcc.spec.bnfparser import MatchScanner
from plcc.spec.bnfrule import Symbol


def test_invalid_tnt():
    with pytest.raises(BnfParser.InvalidTnt):
        BnfParser().parseSymbol(MatchScanner('-'))


def test_terminal():
    tnt = BnfParser().parseSymbol(MatchScanner('HI'))
    assert tnt == Symbol(isTerminal=True, name='HI', alt='', isCapture=False)


def test_captured_terminal():
    tnt = BnfParser().parseSymbol(MatchScanner('<HI>'))
    assert tnt == Symbol(isTerminal=True, name='HI', alt='', isCapture=True)


def test_captured_terminal_with_alt():
    tnt = BnfParser().parseSymbol(MatchScanner('<HI>greet'))
    assert tnt == Symbol(isTerminal=True, name='HI', alt='greet', isCapture=True)


def test_captured_terminal_with_alt_colon():
    tnt = BnfParser().parseSymbol(MatchScanner('<HI>:greet'))
    assert tnt == Symbol(isTerminal=True, name='HI', alt='greet', isCapture=True)


def test_captured_nonterminal():
    tnt = BnfParser().parseSymbol(MatchScanner('<hi>'))
    assert tnt == Symbol(isTerminal=False, name='hi', alt='', isCapture=True)


def test_captured_nonterminal_with_alt():
    tnt = BnfParser().parseSymbol(MatchScanner('<hi>greet'))
    assert tnt == Symbol(isTerminal=False, name='hi', alt='greet', isCapture=True)


def test_captured_nonterminal_with_alt_colon():
    tnt = BnfParser().parseSymbol(MatchScanner('<hi>:greet'))
    assert tnt == Symbol(isTerminal=False, name='hi', alt='greet', isCapture=True)


def test_captured_nonterminal_with_remainder():
    tnt = BnfParser().parseSymbol(MatchScanner('<hi>:greet more stuff'))
    assert tnt == Symbol(isTerminal=False, name='hi', alt='greet', isCapture=True)
