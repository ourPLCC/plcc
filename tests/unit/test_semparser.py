import pytest

from plcc.spec.semparser import SemParser
from plcc.spec.semrule import SemRule
from plcc.spec.specreader import SpecReader
from plcc.spec.line import Line


def toLines(string):
    return SpecReader().readLinesFromString(string)


@pytest.fixture
def parser():
    return SemParser()

def test_(parser):
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
    semRules = list(parser.parse(lines))
    assert semRules[0] == SemRule(
        class_='This',
        modifier=None,
        code=[
            Line(path='', number=3, string='blah', isInBlock=True),
            Line(path='', number=4, string='blah', isInBlock=True)
        ]
    )

    assert semRules[1] == SemRule(
        class_='That',
        modifier='top',
        code=[
        ]
    )
