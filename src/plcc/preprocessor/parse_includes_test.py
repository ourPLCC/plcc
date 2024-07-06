from pytest import raises, mark, fixture


from .parse_lines import parse_lines, Line
from .parse_blocks import parse_blocks, Block, UnclosedBlockError
from .parse_includes import parse_includes, Include


def test_None_yields_nothing():
    assert list(parse_includes(None)) == []


def test_empty_yields_nothing():
    assert list(parse_includes([])) == []


def test_non_includes_pass_through():
    lines = list(parse_blocks(parse_lines('''\
one
%%%
two
%%%
three
''')))
    assert list(parse_includes(lines)) == lines


def test_include():
    lines = list(parse_lines('''\
%include file
'''))
    assert list(parse_includes(lines)) == [
        Include(
            file='file',
            line=Line('%include file', 1, None)
        )
    ]


def test_ignores_includes_in_blocks():
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
