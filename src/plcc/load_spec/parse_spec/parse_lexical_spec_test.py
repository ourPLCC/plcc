from pytest import fixture, raises, mark
from .parse_lexical_spec import parse_lexical_spec, LexicalSpec, LexicalRule
from ..load_rough_spec.parse_lines import Line

def test_empty_yields_nothing():
    lexical_spec = parse_lexical_spec([])
    assert lexical_spec.ruleList == []

def test_None_yields_nothing():
    lexical_spec = parse_lexical_spec(None)
    assert lexical_spec.ruleList == []

def test_blank_lines_skipped():
    lexical_spec = parse_lexical_spec([makeLine('', 1, None)])
    assert lexical_spec.ruleList == []

def test_comment_only_lines_skipped():
    lexical_spec = parse_lexical_spec([makeLine('#This is a test', 1, None), makeLine('   #haha look at me  oubweub', 7, None)])
    assert lexical_spec.ruleList == []

def test_one_skip_token_matched():
    lexical_spec = parse_lexical_spec([makeLine('skip WHITESPACE \',\'', 5, None)])
    assert lexical_spec.ruleList == [makeLexicalRule(makeLine('skip WHITESPACE \',\'', 5, None), True, 'WHITESPACE', ',')]

def test_one_token_matches():
    lexical_spec = parse_lexical_spec([makeLine('token MINUS \'\\-\'', 8, None)])
    assert lexical_spec.ruleList == [makeLexicalRule(makeLine('token MINUS \'\\-\'', 8, None), False, 'MINUS', '\\-')]

def test_one_token_no_token_at_start():
    lexical_spec = parse_lexical_spec([makeLine('MINUS \'\\-\'', 8, None)])
    assert lexical_spec.ruleList == [makeLexicalRule(makeLine('MINUS \'\\-\'', 8, None), False, 'MINUS', '\\-')]

def test_tokens_captured_with_trailing_comment():
    lexical_spec = parse_lexical_spec([makeLine('MINUS \'\\-\'  #This is a test', 8, None), makeLine('token COMMA \',\' #This is also a test', 9, None)])
    assert lexical_spec.ruleList == [makeLexicalRule(makeLine('MINUS \'\\-\'  #This is a test', 8, None), False, 'MINUS', '\\-'), makeLexicalRule(makeLine('token COMMA \',\' #This is also a test', 9, None), False, 'COMMA', ',')]

def test_incorrect_format_is_added_as_a_Line():
    lexical_spec = parse_lexical_spec([makeLine('This line is complete gibberish please ignore', 12, None)])
    assert lexical_spec.ruleList == [makeLine('This line is complete gibberish please ignore', 12, None)]

def test_parser_differentiates_between_Line_and_LexicalRule():
    lexical_spec = parse_lexical_spec([makeLine('This line is even more gibberish', 24, None), makeLine('token LPAREN \'(\'', 23, None)])
    assert lexical_spec.ruleList == [makeLine('This line is even more gibberish', 24, None), makeLexicalRule(makeLine('token LPAREN \'(\'', 23, None), False, 'LPAREN', '(')]

def test_comments_count_as_token_rule():
    lexical_spec = parse_lexical_spec([makeLine('skip COMMENT \'#\'', 2, None)])
    assert lexical_spec.ruleList == [makeLexicalRule(makeLine('skip COMMENT \'#\'', 2, None), True, 'COMMENT', '#')]

def test_comments_at_end_ignored_and_no_comment_is_wrong():
    lexical_spec = parse_lexical_spec([makeLine('skip COMMENT \'%\' #Ironic isn\'t it?', 3, None), makeLine('skip COMMENT \'#\' I forgot the comment', 4, None)])
    assert lexical_spec.ruleList == [makeLexicalRule(makeLine('skip COMMENT \'%\' #Ironic isn\'t it?', 3, None), True, 'COMMENT', '%'), makeLine('skip COMMENT \'#\' I forgot the comment', 4, None)]

def test_token_must_begin_with_no_whitespace():
    lexical_spec = parse_lexical_spec([makeLine('  skip WHITESPACE \',\' ', 1, None)])
    assert lexical_spec.ruleList == [makeLine('  skip WHITESPACE \',\' ', 1, None)]

def makeLexicalRule(line, isSkip, name, pattern):
    return LexicalRule(line, isSkip, name, pattern)

def makeLine(str, lineNumber, file=None):
    return Line(str, lineNumber, file)
