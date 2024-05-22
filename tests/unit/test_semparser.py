import pytest

from plcc.specfile.semparser import SemParser
from plcc.specfile.semrule import SemRule
from plcc.specfile.reader import SpecFileReader
from plcc.specfile.line import Line


def toLines(string):
    return SpecFileReader().readLinesFromString(string)


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
