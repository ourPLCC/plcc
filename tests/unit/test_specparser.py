import pytest

from plcc.spec.reader import SpecReader
from plcc.spec.specparser import SpecParser
from plcc.spec.spec import Spec


@pytest.fixture
def parser():
    return SpecParser()


def toLines(string):
    return SpecReader().readLinesFromString(string)


def test_parser(parser):
    lines = toLines(
        'skip WS "\s+"\n'
        'token HI "hi"\n'
        '%\n'
        '<hi> ::= HI\n'
        '%\n'
        'Hi\n'
        '%%%\n'
        'public void greet() { System.out.println("hi"); }\n'
        '%%%\n'
    )

