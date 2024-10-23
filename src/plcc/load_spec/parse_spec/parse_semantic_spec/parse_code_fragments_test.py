from pytest import raises
from .parse_code_fragments import CodeFragment, parse_code_fragments, UndefinedTargetLocatorError, DuplicateTargetLocatorError, CodeFragmentMissingBlockError
from .parse_target_locator import TargetLocator, InvalidTargetLocatorError
from plcc.load_spec.load_rough_spec.parse_blocks import Block
from plcc.load_spec.load_rough_spec.parse_lines import Line, parse_lines

def test_basic():
    lines_and_blocks = [make_line('Class:init'), make_block()]
    assert parse_code_fragments(lines_and_blocks) == [
        CodeFragment(make_target_locator(lines_and_blocks[0], 'Class', 'init'), make_block())]

def test_consecutive():
    lines_and_blocks = [make_line('Class:init'), make_block(), make_line('Main'), make_block()]
    assert parse_code_fragments(lines_and_blocks) == [
        CodeFragment(make_target_locator(lines_and_blocks[0], 'Class', 'init'), make_block()),
        CodeFragment(make_target_locator(lines_and_blocks[2], 'Main', None), make_block())]

def test_input_must_be_Lines_and_Blocks():
    invalid_input = ["Only Lines and Dividers Work!", make_line('Class'), make_block()]
    with raises(TypeError):
        parse_code_fragments(invalid_input)

def test_blank_lines_ignored():
    lines = [make_line('Class:init'), make_line('\n'), make_line(''), make_block()]
    assert parse_code_fragments(lines) == [
        CodeFragment(make_target_locator(lines[0], 'Class', 'init'), make_block())]

def test_consecutive_target_locators_raise_error():
    lines_and_blocks = [make_line('Class:init'), make_line('Class:init'), make_block()]
    with raises(DuplicateTargetLocatorError):
        parse_code_fragments(lines_and_blocks)

def test_blocks_cannot_be_adjacent():
    with raises(UndefinedTargetLocatorError):
      parse_code_fragments([make_line('Class:init'), make_block(), make_block()])

def test_target_locator_without_block_raise_error():
    with raises(CodeFragmentMissingBlockError):
        parse_code_fragments([make_line('Class:init')])

def test_block_must_have_target_locator():
    with raises(UndefinedTargetLocatorError):
        parse_code_fragments([make_block()])

def make_target_locator(line, className, modifier):
    return TargetLocator(line, className, modifier)

def make_block():
    return  Block(list(parse_lines('''\
%%%
block
%%%
''')))

def make_line(string, number=1, file=None):
    return Line(string, number, file)
