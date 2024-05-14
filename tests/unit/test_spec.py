import pytest


from plcc.spec import parse
from plcc.spec import LexRule
from plcc.specfile.line import Line


def test_parse_wrong_type(fs):
    with pytest.raises(TypeError):
        parse(None)


def lines(string):
    return iter([Line(string=s, path='', number=i) for i, s in enumerate(string.splitlines(), start=1)])


def test_parse_skip_rule(fs):
    spec = parse(lines(r"skip WS '\s+'"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='skip', name='WS', pattern=r'\s+', quote="'", end="", line=Line(string=r"skip WS '\s+'", path='', number=1))


def test_parse_token_rule(fs):
    spec = parse(lines(r"token WS '\s+'"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote="'", end="", line=Line(string=r"token WS '\s+'", path='', number=1))


def test_parse_implicit_token_rule(fs):
    spec = parse(lines(r"WS '\s+'"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote="'", end="", line=Line(string=r"WS '\s+'", path='', number=1))


def test_allow_line_comment_in_lex_rule(fs):
    spec = parse(lines(r"WS '\s+' # hi"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote="'", end=" # hi", line=Line(string=r"WS '\s+' # hi", path='', number=1))


def test_allow_pound_in_lex_rule_pattern(fs):
    spec = parse(lines(r"COMMENT ' #\s+' # matching a comment"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='COMMENT', pattern=r' #\s+', quote="'", end=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=1))


def test_skip_blank_lines_in_lex(fs):
    spec = parse(lines("\n\nCOMMENT ' #\\s+' # matching a comment"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='COMMENT', pattern=r' #\s+', quote="'", end=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=3))


def test_skip_comment_lines_in_lex(fs):
    spec = parse(lines("#one\n  # two \nCOMMENT ' #\\s+' # matching a comment"))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='COMMENT', pattern=r' #\s+', quote="'", end=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=3))


def test_allow_double_quote_in_lex(fs):
    spec = parse(lines(r'WS "\s+"'))
    rules = spec.getLexRules()
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote='"', end="", line=Line(string=r'WS "\s+"', path='', number=1))


