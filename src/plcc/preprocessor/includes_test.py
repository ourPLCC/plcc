from pytest import raises, mark, fixture


from .lines import parse_lines, Line
from .blocks import parse_blocks, Block, UnclosedBlockError
from .includes import parse_includes, Include


def test_parse_includes_None_yields_nothing():
    assert list(parse_includes(None)) == []


def test_parse_includes_empty_yields_nothing():
    assert list(parse_includes([])) == []


def test_parse_includes_non_includes_pass_through():
    lines = list(parse_blocks(parse_lines('''\
one
%%%
two
%%%
three
''')))
    assert list(parse_includes(lines)) == lines


def test_parse_includes_include():
    lines = list(parse_lines('''\
%include file
'''))
    assert list(parse_includes(lines)) == [
        Include(
            file='file',
            line=Line('%include file', 1, None)
        )
    ]


def test_parse_includes_ignore_includes_in_blocks():
    lines = list(parse_blocks(parse_lines('''\
%%%
%include file
%%%
''')))
    assert list(parse_includes(lines)) == [
        Block(
            [
                Line('%%%', 1, None),
                Line('%include file', 2, None),
                Line('%%%', 3, None)
            ]
        )
    ]
