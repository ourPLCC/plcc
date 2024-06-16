from pytest import fixture, mark, raises


from . import BlockMarker
from . import LineInBlock
from . import markLineInBlock
from . import UnclosedBlockError


from ..read_lines import toLines
from ..read_lines import Line


@fixture
def marker():
    return BlockMarker()


def test_empty(marker):
    assert marker.mark([]) == []


def test_no_block(marker):
    given = [
        'one',
        'two'
    ]
    assert marker.mark(toLines(given)) == toBlockLines(given)


def test_triple_percent(marker):
    marked = marker.mark(toLines([
        '%%%',
        'one',
        '%%%',
        'two',
        '%%%',
        'three',
        'four',
        '%%%'
    ]))
    assert isinstance(marked[1], LineInBlock)
    assert marked == toBlockLines([
        '%%%',
        '>>>one',
        '%%%',
        'two',
        '%%%',
        '>>>three',
        '>>>four',
        '%%%'
    ])


def test_unclosed_block(marker):
    with raises(UnclosedBlockError) as info:
        marker.mark(toLines([
            '%%%',
            'one',
            '%%%',
            'two',
            '%%%',
            'three',
            'four'
        ]))

    e = info.value
    assert e.unclosedBlockStartLine == Line(string='%%%', number=5, file='')


def test_percent_percent_curly(marker):
    marked = marker.mark(toLines([
        '%%{',
        'one',
        '%%}',
        'two',
        '%%{',
        'three',
        'four',
        '%%}'
    ]))

    assert isinstance(marked[1], LineInBlock)
    assert marked == toBlockLines([
        '%%{',
        '>>>one',
        '%%}',
        'two',
        '%%{',
        '>>>three',
        '>>>four',
        '%%}'
    ])


def test_no_mixed_brackets(marker):
    with raises(UnclosedBlockError) as info:
        marker.mark(toLines([
            '%%{',
            'one',
            '%%%',
        ]))
    e = info.value
    assert e.unclosedBlockStartLine == Line(string='%%{', number=1, file='')



def toBlockLines(strings):
    return [ markLineInBlock(line(s[3:],k)) if s.startswith('>>>') else line(s,k) for k,s in enumerate(strings, start=1)]


def line(s, k):
    return Line(string=s, number=k, file='')
