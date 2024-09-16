from pytest import raises, mark, fixture

from .parse_lines import Line
from .parse_dividers import Divider
from .load_rough_spec import load_rough_spec
from .split_rough_spec import RoughSpec, split_rough_spec


def test_empty():
    rough_spec = []
    expected = RoughSpec(
        lexicalSection=[],
        syntacticSection=[],
        semanticSectionList=[]
    )

    res = split_rough_spec(rough_spec)
    assert res == expected


def test_no_divider():
    rough_spec = makeLineList('''
        one
        two
        three
    ''')

    expected = RoughSpec(
        lexicalSection=rough_spec[:],
        syntacticSection=[],
        semanticSectionList=[]
    )

    res = split_rough_spec(rough_spec)
    assert res == expected


def test_one_divider():
    rough_spec = [
        makeLine('one'),
        makeDivider('%'),
        makeLine('two'),
        makeLine('three')
    ]
    expected = RoughSpec(
        lexicalSection=rough_spec[:1],
        syntacticSection=rough_spec[1:],
        semanticSectionList=[]
    )
    res = split_rough_spec(rough_spec)
    assert res == expected


def test_three_dividers():
    rough_spec = [
        makeLine('one'),
        makeDivider('%'),
        makeLine('two'),
        makeDivider('%'),
        makeLine('three')
    ]

    expected = RoughSpec(
        lexicalSection=rough_spec[0:1],
        syntacticSection=rough_spec[1:3],
        semanticSectionList=[
            rough_spec[3:5]
        ]
    )

    res = split_rough_spec(rough_spec)
    assert res == expected


def test_multiple_semantic_sections():
    rough_spec = [
        makeLine('one'),
        makeDivider('%'),
        makeLine('two'),
        makeDivider('%'),
        makeLine('three'),
        makeDivider('%'),
        makeLine('four')
    ]

    expected = RoughSpec(
        lexicalSection=rough_spec[0:1],
        syntacticSection=rough_spec[1:3],
        semanticSectionList=[
            rough_spec[3:5],
            rough_spec[5:7]
        ]
    )

    res = split_rough_spec(rough_spec)
    assert res == expected


def makeLineList(string):
    return [makeLine(s.strip()) for s in string.strip().split('\n')]


def makeDivider(string):
    return Divider(makeLine(string))


def makeLine(string):
    return Line(string, None, None)
