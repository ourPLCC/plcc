import pytest


from plcc.specfile.lexparse import parse, LexRule
from plcc.specfile.line import Line


def test_parse_wrong_type(fs):
    with pytest.raises(TypeError):
        parse(None)


def lines(string):
    return iter([Line(string=s, path='', number=i) for i, s in enumerate(string.splitlines(), start=1)])


def test_parse_skip_rule():
    rules = parse(lines(r"skip WS '\s+'"))
    assert rules[0] == LexRule(type='skip', name='WS', pattern=r'\s+', quote="'", end="", line=Line(string=r"skip WS '\s+'", path='', number=1))


def test_parse_token_rule():
    rules = parse(lines(r"token WS '\s+'"))
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote="'", end="", line=Line(string=r"token WS '\s+'", path='', number=1))


def test_parse_implicit_token_rule():
    rules = parse(lines(r"WS '\s+'"))
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote="'", end="", line=Line(string=r"WS '\s+'", path='', number=1))


def test_allow_line_comment_in_lex_rule():
    rules = parse(lines(r"WS '\s+' # hi"))
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote="'", end=" # hi", line=Line(string=r"WS '\s+' # hi", path='', number=1))


def test_allow_pound_in_lex_rule_pattern():
    rules = parse(lines(r"COMMENT ' #\s+' # matching a comment"))
    assert rules[0] == LexRule(type='token', name='COMMENT', pattern=r' #\s+', quote="'", end=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=1))


def test_skip_blank_lines_in_lex():
    rules = parse(lines("\n\nCOMMENT ' #\\s+' # matching a comment"))
    assert rules[0] == LexRule(type='token', name='COMMENT', pattern=r' #\s+', quote="'", end=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=3))


def test_skip_comment_lines_in_lex():
    rules = parse(lines("#one\n  # two \nCOMMENT ' #\\s+' # matching a comment"))
    assert rules[0] == LexRule(type='token', name='COMMENT', pattern=r' #\s+', quote="'", end=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=3))


def test_allow_double_quote_in_lex():
    rules = parse(lines(r'WS "\s+"'))
    assert rules[0] == LexRule(type='token', name='WS', pattern=r'\s+', quote='"', end="", line=Line(string=r'WS "\s+"', path='', number=1))


def test_lex_combined_example():
    rules = parse(lines(r'''# A typical example
skip WS "\s+"
  # This line is ignored, as is the blank line below.
token HI 'hi'   # for a greeting

BYE " # " # we're "pounding (#)" it out
'''))
    assert rules[0] == LexRule(type='skip', name='WS', pattern=r'\s+', quote='"', end="", line=Line(string=r'skip WS "\s+"', path='', number=2))
    assert rules[1] == LexRule(type='token', name='HI', pattern=r'hi', quote="'", end="   # for a greeting", line=Line(string=r"token HI 'hi'   # for a greeting", path='', number=4))
    assert rules[2].end.startswith(' # ')
