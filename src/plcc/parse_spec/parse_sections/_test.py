from unittest.mock import Mock


from pytest import fixture, raises, mark


from . import SectionParser
from ..read_file import toLines


class MockSectionBuilder:
    def __init__(self):
        self.calls=''

    def start(self):
        self.calls += 'S'

    def line(self, line):
        self.calls += 'L'

    def divider(self, line):
        self.calls += 'D'

    def openCode(self, line):
        self.calls += 'O'

    def closeCode(self, line):
        self.calls += 'C'

    def codeLine(self, line):
        self.calls += 'c'

@fixture
def builder():
    return MockSectionBuilder()


@fixture
def parser(builder):
    return SectionParser(builder)


def test_empty(parser):
    parser.parse([])
    assert parser.builder.calls == ''


def test_one_line(parser):
    parser.parse(toLines(['one']))
    assert parser.builder.calls == 'SL'


def test_two_lines(parser):
    parser.parse(toLines(['one', 'two']))
    assert parser.builder.calls == 'SLL'


def test_two_empty_sections(parser):
    parser.parse(toLines(['%']))
    assert parser.builder.calls == 'SD'


def test_three_empty_sections(parser):
    parser.parse(toLines(['%', '%']))
    assert parser.builder.calls == 'SDD'


def test_block_lines(parser):
    parser.parse(toLines(['%%%', 'blah', '%%%']))
    assert parser.builder.calls == 'SOcC'


def test_ignore_divider_in_code(parser):
    parser.parse(toLines(['%%%', '%', '%%%']))
    assert parser.builder.calls == 'SOcC'

