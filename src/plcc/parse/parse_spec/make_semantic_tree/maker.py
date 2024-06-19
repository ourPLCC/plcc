from __future__ import annotations


from ...read_sections import Line
from .tree import SemanticTree
from .builder import SemanticTreeBuilder
from .parser import parse


def make_semantic_tree(lines: str|[str]|Line) -> SemanticTree:
    b = SemanticTreeBuilder()
    parse(b, lines)
    return b.result
