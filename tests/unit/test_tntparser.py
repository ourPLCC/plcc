import pytest

from plcc.specfile.line import toLines
from plcc.specfile.bnfparse import TntParser, Tnt


def test_invalid_tnt():
    with pytest.raises(TntParser.InvalidTnt):
        TntParser().parse('-')


def test_invalid_terminal():
    with pytest.raises(TntParser.InvalidTerminal):
        TntParser().parse('abc')


def test_terminal():
    tnt, remainder = TntParser().parse('HI')
    assert tnt == Tnt(type='terminal', name='HI', alt='', capture=False)
    assert remainder == ''


def test_captured_terminal():
    tnt, remainder = TntParser().parse('<HI>')
    assert tnt == Tnt(type='terminal', name='HI', alt='', capture=True)
    assert remainder == ''


def test_captured_terminal_with_alt():
    tnt, remainder = TntParser().parse('<HI>greet')
    assert tnt == Tnt(type='terminal', name='HI', alt='greet', capture=True)
    assert remainder == ''


def test_captured_terminal_with_alt_colon():
    tnt, remainder = TntParser().parse('<HI>:greet')
    assert tnt == Tnt(type='terminal', name='HI', alt='greet', capture=True)
    assert remainder == ''


def test_captured_nonterminal():
    tnt, remainder = TntParser().parse('<hi>')
    assert tnt == Tnt(type='nonterminal', name='hi', alt='', capture=True)
    assert remainder == ''


def test_captured_nonterminal_with_alt():
    tnt, remainder = TntParser().parse('<hi>greet')
    assert tnt == Tnt(type='nonterminal', name='hi', alt='greet', capture=True)
    assert remainder == ''


def test_captured_nonterminal_with_alt_colon():
    tnt, remainder = TntParser().parse('<hi>:greet')
    assert tnt == Tnt(type='nonterminal', name='hi', alt='greet', capture=True)
    assert remainder == ''


def test_captured_nonterminal_with_remainder():
    tnt, remainder = TntParser().parse('<hi>:greet more stuff')
    assert tnt == Tnt(type='nonterminal', name='hi', alt='greet', capture=True)
    assert remainder == ' more stuff'
