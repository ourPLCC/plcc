import pytest

from plcc.parser.semparser import SemParser
from plcc.spec.semrule import SemRule
from plcc.parser.specreader import SpecReader
from plcc.spec.line import Line


def toLines(string):
    return SpecReader().readLinesFromString(string)


@pytest.fixture
def parser():
    return SemParser()


def test_typical_case(parser):
    lines = toLines(
        'This\n'
        '%%%\n'
        'blah\n'
        'blah\n'
        '%%%\n'
        '\n'
        'That:top\n'
        '%%%\n'
        '%%%\n'
    )
    semRules = list(parser.parseIntoSemRules(lines))
    assert semRules[0] == SemRule(
        class_='This',
        modifier=None,
        code=[
            Line(path='', number=3, string='blah', isInCodeBlock=True),
            Line(path='', number=4, string='blah', isInCodeBlock=True)
        ]
    )

    assert semRules[1] == SemRule(
        class_='That',
        modifier='top',
        code=[
        ]
    )


def test_invalid_class_line(parser):
    lines = toLines(
        'This:Not Good\n'
        '%%%\n'
        'blah\n'
        'blah\n'
        '%%%\n'
    )
    with pytest.raises(SemParser.InvalidSemRule):
        list(parser.parseIntoSemRules(lines))
