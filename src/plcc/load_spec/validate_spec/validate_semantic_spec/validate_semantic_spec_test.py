from pytest import raises, mark, fixture
from .validate_semantic_spec import InvalidClassNameError, validate_semantic_spec
from ...parse_spec.parse_semantic_spec import SemanticSpec, parse_semantic_spec
from ...load_rough_spec.parse_lines import Line, parse_lines
from ...load_rough_spec.parse_dividers import Divider
from ...load_rough_spec.parse_blocks import Block



def test_valid_names_no_errors():
    assertValidClassNames(["Class","CLASS","C_lass_","C123","C", "ClaSs", "C_la55"])

def test_no_code_fragments_no_errors():
    semanticSpec = makeSemanticSpec([])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 0

def test_begin_lowercase_format_error():
    assertInvalidClassName("startsLowerCase")

def test_begin_number_format_error():
    assertInvalidClassName("12MustStartUppercase")

def test_whitespace_name_format_error():
    assertInvalidClassName("White Space")

def test_multiple_errors_all_counted():
    assertMultipleInvalidClassNames(["123StartsWithNumbers", "notuppercase", "InvalidChar`", "Invalid space"])

def test_valid_and_invalid_names():
    semanticSpec = makeSemanticSpec([makeLine("Class"), makeBlock(), makeLine("invalid"), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidClassNameError("invalid")

def assertValidClassNames(names: list[str]):
    for name in names:
        assertValidClassName(name)

def assertValidClassName(name: str):
    semanticSpec = makeSemanticSpec([makeLine(name), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 0

def assertInvalidClassName(name: str):
    semanticSpec = makeSemanticSpec([makeLine(name), makeBlock()])
    errors = validate_semantic_spec(semanticSpec)
    assert len(errors) == 1
    assert errors[0] == makeInvalidClassNameError(name)

def assertMultipleInvalidClassNames(strings):
    lines_and_blocks = makeLinesAndBlocksFromStrings(strings)
    semanticSpec = makeSemanticSpec(lines_and_blocks)
    errors = validate_semantic_spec(semanticSpec)
    for i, obj in enumerate(lines_and_blocks):
        if type(obj) is Block:
            return
        assert errors[i] == makeInvalidClassNameError(obj.string)
    else: # pragma: no cover
        pass


def makeLinesAndBlocksFromStrings(strings: list[str]) -> list[Line | Block]:
    lines_and_blocks = []
    for string in strings:
        lines_and_blocks.append(makeLine(string))
        lines_and_blocks.append(makeBlock())
    return lines_and_blocks

def makeInvalidClassNameError(name: str):
    return InvalidClassNameError(
        makeLine(name),
        f"Invalid name format for ClassName {name}, (Must start with an upper case letter, and may contain upper or lower case letters, numbers, and underscores).")

def makeSemanticSpec(linesAndBlocks: list[Line | Block]):
    return parse_semantic_spec([makeDivider('Java', 'Java', makeLine("%"))] + linesAndBlocks)

def makeLine(string, lineNumber=1, file=None):
    return Line(string, lineNumber, file)

def makeBlock():
    return  Block(list(parse_lines('''\
%%%
block
%%%
''')))

def makeDivider(tool, language, line):
    return Divider(tool=tool, language=language, line=line)
