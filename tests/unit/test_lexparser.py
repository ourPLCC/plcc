import pytest


from plcc.spec.lexparser import LexParser
from plcc.spec.lexrule import LexRule
from plcc.spec.line import Line
from plcc.spec.specreader import SpecReader


@pytest.fixture
def parser():
    return LexParser()


def test_parse_wrong_type(parser, fs):
    rules = parser.parse(None)
    with pytest.raises(TypeError):
        next(rules)


def lines(string):
    return SpecReader().readLinesFromString(string)


def test_parse_skip_rule(parser):
    rules = parser.parse(lines(r"skip WS '\s+'"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=False, name='WS', pattern=r'\s+', remainder="", line=Line(string=r"skip WS '\s+'", path='', number=1))


def test_parse_token_rule(parser):
    rules = parser.parse(lines(r"token WS '\s+'"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='WS', pattern=r'\s+', remainder="", line=Line(string=r"token WS '\s+'", path='', number=1))


def test_parse_implicit_token_rule(parser):
    rules = parser.parse(lines(r"WS '\s+'"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='WS', pattern=r'\s+', remainder="", line=Line(string=r"WS '\s+'", path='', number=1))


def test_allow_line_comment_in_lex_rule(parser):
    rules = parser.parse(lines(r"WS '\s+' # hi"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='WS', pattern=r'\s+', remainder=" # hi", line=Line(string=r"WS '\s+' # hi", path='', number=1))


def test_allow_pound_in_lex_rule_pattern(parser):
    rules = parser.parse(lines(r"COMMENT ' #\s+' # matching a comment"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='COMMENT', pattern=r' #\s+', remainder=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=1))


def test_skip_blank_lines_in_lex(parser):
    rules = parser.parse(lines("\n\nCOMMENT ' #\\s+' # matching a comment"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='COMMENT', pattern=r' #\s+', remainder=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=3))


def test_skip_comment_lines_in_lex(parser):
    rules = parser.parse(lines("#one\n  # two \nCOMMENT ' #\\s+' # matching a comment"))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='COMMENT', pattern=r' #\s+', remainder=" # matching a comment", line=Line(string=r"COMMENT ' #\s+' # matching a comment", path='', number=3))


def test_allow_double_quote_in_lex(parser):
    rules = parser.parse(lines(r'WS "\s+"'))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=True, name='WS', pattern=r'\s+', remainder="", line=Line(string=r'WS "\s+"', path='', number=1))


def test_lex_combined_example(parser):
    rules = parser.parse(lines(r'''# A typical example
skip WS "\s+"
  # This line is ignored, as is the blank line below.
token HI 'hi'   # for a greeting

BYE " # " # we're "pounding (#)" it out
'''))
    rules = list(rules)
    assert rules[0] == LexRule(isToken=False, name='WS', pattern=r'\s+', remainder="", line=Line(string=r'skip WS "\s+"', path='', number=2))
    assert rules[1] == LexRule(isToken=True, name='HI', pattern=r'hi', remainder="   # for a greeting", line=Line(string=r"token HI 'hi'   # for a greeting", path='', number=4))
    assert rules[2].remainder.startswith(' # ')
