import pytest

from plcc.specfile.line import strToLines
from plcc.specfile.semparse import SemParser, SemRule


@pytest.mark.xfail
def test_standard():
    lines = list(strToLines(
        'One\n'
        '%%%\n'
        'whatever\n'
        'more whatever\n'
        '%%%\n'
    ))
    rules = list(SemParser().parse(lines))
    assert len(rules) == 1
    assert rules == [
        SemRule(
            class_='One',
            hook='default',
            code=[
                'whatever',
                'more whatever'
            ]
        )
    ]
