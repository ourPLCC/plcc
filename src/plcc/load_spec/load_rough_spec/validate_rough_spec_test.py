from pytest import raises, mark, fixture

from .parse_lines import Line
from .parse_blocks import Block
from .split_rough_spec import RoughSpec
from .validate_rough_spec import ValidationError, validate_rough_spec


def test_empty_spec_produces_no_errors():
    spec = makeRoughSpec()
    errors = validate_rough_spec(spec)
    assert len(errors) == 0


def test_block_in_lexical_section_errors():
    block = makeEmptyBlock()
    spec = makeRoughSpec(
        lexicalSection=[
            block
        ]
    )
    errors = validate_rough_spec(spec)
    assert errors[0] == makeLexicalValidationError(block.lines[0])


def test_non_blocks_do_not_cause_an_error():
    block = makeEmptyBlock()
    spec = makeRoughSpec(
        lexicalSection=[
            makeLine('not a block')
        ],
        syntacticSection=[
            makeLine('not a block either')
        ]

    )
    errors = validate_rough_spec(spec)
    assert len(errors) == 0


def test_block_in_syntactic_section_errors():
    block = makeEmptyBlock()
    spec = makeRoughSpec(
        syntacticSection=[
            block
        ]
    )
    errors = validate_rough_spec(spec)
    assert errors[0] == makeSyntacticValidationError(block.lines[0])


def test_block_in_semantic_section_is_NOT_an_error():
    block = makeEmptyBlock()
    spec = makeRoughSpec(
        semanticSectionList=[
            [ block ]
        ]
    )
    errors = validate_rough_spec(spec)
    assert len(errors) == 0


def test_multiple_errors():
    block1 = makeEmptyBlock(startNumber=1)
    block2 = makeEmptyBlock(startNumber=5)
    block3 = makeEmptyBlock(startNumber=10)
    spec = makeRoughSpec(
        lexicalSection=[
            block1
        ],
        syntacticSection=[
            block2,
            block3
        ]
    )
    errors = validate_rough_spec(spec)
    assert errors[0] == makeLexicalValidationError(block1.lines[0])
    assert errors[1] == makeSyntacticValidationError(block2.lines[0])
    assert errors[2] == makeSyntacticValidationError(block3.lines[0])


def makeEmptyBlock(startNumber=1):
    return makeBlock(
        makeLines('''
            %%%
            %%%
        ''', startNumber)
    )


def makeRoughSpec(lexicalSection=None, syntacticSection=None, semanticSectionList=None):
    lexicalSection = lexicalSection if lexicalSection else []
    syntacticSection = syntacticSection if syntacticSection else []
    semanticSectionList = semanticSectionList if semanticSectionList else []
    return RoughSpec(lexicalSection, syntacticSection, semanticSectionList)


def makeLines(string, startNumber=1):
    numbers = iter(range(startNumber, 100000))
    return [makeLine(s.strip(), lineNumber=next(numbers)) for s in string.strip().split('\n')]


def makeLine(string, lineNumber=1):
    return Line(string, lineNumber, None)


def makeBlock(lines):
    return Block(lines)


def makeLexicalValidationError(line):
    return makeValidationError('lexical', line)


def makeSyntacticValidationError(line):
    return makeValidationError('syntactic', line)


def makeValidationError(section, line):
    return ValidationError(line, f"The {section} section must not have a Block: {line}")
