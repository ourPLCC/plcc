import pytest


from plcc.parser.bnfparser import BnfParser
from plcc.parser.bnfparser import InvalidSymbol
from plcc.parser.bnfparser import InvalidLeftHandSide
from plcc.spec.bnfrule import Symbol


def parseSymbolInString(string):
    symbol, remainder = BnfParser().parseSymbol(string)
    return symbol


def test_invalid_symbol():
    with pytest.raises(InvalidSymbol):
        parseSymbolInString('-')


def test_terminal():
    symbol = parseSymbolInString('HI')
    assert symbol == Symbol(isTerminal=True, name='HI', alt='', isCapture=False)


def test_captured_terminal():
    symbol = parseSymbolInString('<HI>')
    assert symbol == Symbol(isTerminal=True, name='HI', alt='', isCapture=True)


def test_captured_terminal_with_alt():
    symbol = parseSymbolInString('<HI>greet')
    assert symbol == Symbol(isTerminal=True, name='HI', alt='greet', isCapture=True)


def test_captured_terminal_with_alt_colon():
    symbol = parseSymbolInString('<HI>:greet')
    assert symbol == Symbol(isTerminal=True, name='HI', alt='greet', isCapture=True)


def test_captured_nonterminal():
    symbol = parseSymbolInString('<hi>')
    assert symbol == Symbol(isTerminal=False, name='hi', alt='', isCapture=True)


def test_captured_nonterminal_with_alt():
    symbol = parseSymbolInString('<hi>greet')
    assert symbol == Symbol(isTerminal=False, name='hi', alt='greet', isCapture=True)


def test_captured_nonterminal_with_alt_colon():
    symbol = parseSymbolInString('<hi>:greet')
    assert symbol == Symbol(isTerminal=False, name='hi', alt='greet', isCapture=True)


def test_captured_nonterminal_with_remainder():
    symbol = parseSymbolInString('<hi>:greet more stuff')
    assert symbol == Symbol(isTerminal=False, name='hi', alt='greet', isCapture=True)
