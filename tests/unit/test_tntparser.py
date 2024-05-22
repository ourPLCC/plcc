import pytest

from plcc.specfile.bnfparser import MatchScanner, TntParser, Tnt



def test_invalid_tnt():
    with pytest.raises(TntParser.InvalidTnt):
        TntParser().parse(MatchScanner('-'))



def test_invalid_terminal():
    with pytest.raises(TntParser.InvalidTerminal):
        TntParser().parse(MatchScanner('abc'))



def test_terminal():
    tnt = TntParser().parse(MatchScanner('HI'))
    assert tnt == Tnt(type='terminal', name='HI', alt='', capture=False)



def test_captured_terminal():
    tnt = TntParser().parse(MatchScanner('<HI>'))
    assert tnt == Tnt(type='terminal', name='HI', alt='', capture=True)



def test_captured_terminal_with_alt():
    tnt = TntParser().parse(MatchScanner('<HI>greet'))
    assert tnt == Tnt(type='terminal', name='HI', alt='greet', capture=True)



def test_captured_terminal_with_alt_colon():
    tnt = TntParser().parse(MatchScanner('<HI>:greet'))
    assert tnt == Tnt(type='terminal', name='HI', alt='greet', capture=True)



def test_captured_nonterminal():
    tnt = TntParser().parse(MatchScanner('<hi>'))
    assert tnt == Tnt(type='nonterminal', name='hi', alt='', capture=True)



def test_captured_nonterminal_with_alt():
    tnt = TntParser().parse(MatchScanner('<hi>greet'))
    assert tnt == Tnt(type='nonterminal', name='hi', alt='greet', capture=True)



def test_captured_nonterminal_with_alt_colon():
    tnt = TntParser().parse(MatchScanner('<hi>:greet'))
    assert tnt == Tnt(type='nonterminal', name='hi', alt='greet', capture=True)



def test_captured_nonterminal_with_remainder():
    tnt = TntParser().parse(MatchScanner('<hi>:greet more stuff'))
    assert tnt == Tnt(type='nonterminal', name='hi', alt='greet', capture=True)
