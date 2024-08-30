from __future__ import annotations


from ...read_sections import Line
from .tree import SyntacticTree
from .builder import SyntacticTreeBuilder
from .parser import parse


def make_syntactic_tree(lines: str|[str]|[Line]) -> SyntacticTree:
    builder = SyntacticTreeBuilder()
    parse(builder, lines)
    return builder.result
