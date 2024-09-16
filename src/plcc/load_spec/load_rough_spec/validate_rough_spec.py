from dataclasses import dataclass

from .parse_lines import Line
from .parse_dividers import Divider
from .parse_blocks import Block
from .split_rough_spec import RoughSpec


@dataclass
class ValidationError:
    line: Line
    message: str


def validate_rough_spec(rough_spec:RoughSpec):
    errorList = []
    errorList.extend(check_no_blocks_in_lexicalSection(rough_spec))
    errorList.extend(check_no_blocks_in_syntacticSection(rough_spec))
    return errorList


def check_no_blocks_in_lexicalSection(rough_spec:RoughSpec):
    errorList = []
    for i in rough_spec.lexicalSection:
        if isinstance(i, Block):
            m = f"The lexical section must not have a Block: {i.lines[0]}"
            errorList.append(ValidationError(line=i.lines[0], message=m))
    return errorList


def check_no_blocks_in_syntacticSection(rough_spec:RoughSpec):
    errorList = []
    for i in rough_spec.syntacticSection:
        if isinstance(i, Block):
            m = f"The syntactic section must not have a Block: {i.lines[0]}"
            errorList.append(ValidationError(line=i.lines[0], message=m))
    return errorList
