from pytest import raises, mark, fixture


from .parse_lines import parse_lines, Line
from .parse_blocks import parse_blocks, Block, UnclosedBlockError
from .parse_dividers import parse_dividers, Divider


def test_None_yields_nothing():
    assert list(parse_dividers(None)) == []


def test_empty_yields_nothing():
    assert list(parse_dividers([])) == []


def test_non_dividers_pass_through():
    lines = list(parse_blocks(parse_lines('''\
one
%%%
two
%%%
three
''')))
    assert list(parse_dividers(lines)) == lines


def test_one_divider():
    lines = list(parse_lines('%'))
    assert list(parse_dividers(lines)) == [
        Divider(Line('%', 1, None)),
    ]


def test_one_divider_with_trailing_content():
    lines = list(parse_lines('% trailing'))
    assert list(parse_dividers(lines)) == [
        Divider(Line('% trailing', 1, None)),
    ]


def test_two_percents_does_not_match():
    lines = list(parse_lines('%%'))
    assert list(parse_dividers(lines)) == [
        Line('%%', 1, None),
    ]


def test_blocks_mask_dividers():
    lines = list(parse_blocks(parse_lines('%%%\n%\n%%%')))
    assert list(parse_dividers(lines)) == [
        Block([
            Line('%%%', 1, None),
            Line('%', 2, None),
            Line('%%%', 3, None)
        ])
    ]

