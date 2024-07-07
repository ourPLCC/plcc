from pytest import raises, mark, fixture


from .parse_lines import parse_lines, Line
from .parse_blocks import parse_blocks, Block, UnclosedBlockError
from .parse_includes import parse_includes, Include
from .process_includes import process_includes, CircularIncludeError


def test_None_yields_nothing():
    assert list(process_includes(None)) == []


def test_empty_yields_nothing():
    assert list(process_includes([])) == []


def test_no_includes_pass_through():
    lines = list(parse_lines('one\ntwo\nthree'))
    assert list(process_includes(lines)) == lines


def test_include(fs):
    fs.create_file('/f', contents='hi')
    assert list(process_includes(parse_includes(parse_lines('%include /f')))) == [
        Line('hi', 1, '/f')
    ]

def test_circular_include_errors(fs):
    fs.create_file('/f', contents='%include /f')
    with raises(CircularIncludeError):
        list(process_includes(parse_includes(parse_lines('%include /f'))))
