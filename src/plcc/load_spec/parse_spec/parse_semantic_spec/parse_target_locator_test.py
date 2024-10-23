from pytest import raises
from .parse_target_locator import TargetLocator, parse_target_locator, InvalidTargetLocatorError
from plcc.load_spec.load_rough_spec.parse_lines import Line, parse_lines

def test_ignore_EOL_comments():
    line = make_line('Class:init #comment')
    assert parse_target_locator(line) == TargetLocator(line, 'Class', 'init')

def test_className_accepts_any_character():
    line = make_line('1*~=^RandomStuff')
    assert parse_target_locator(line) == TargetLocator(line, '1*~=^RandomStuff', None)

def test_modifier():
    lines = [make_line('Class:init'), make_line('Class:modifier')]
    assert parse_target_locator(lines[0]) == TargetLocator(lines[0], 'Class', 'init')
    assert parse_target_locator(lines[1]) == TargetLocator(lines[1], 'Class', 'modifier')

def test_empty_line_raises_error():
    with raises(InvalidTargetLocatorError):
        parse_target_locator(make_line(''))

def test_className():
    lines = [make_line('Class'), make_line('name')]
    assert parse_target_locator(lines[0]) == TargetLocator(lines[0], 'Class', None)
    assert parse_target_locator(lines[1]) == TargetLocator(lines[1], 'name', None)

def make_line(string, number=1, file=None):
    return Line(string, number, file)
