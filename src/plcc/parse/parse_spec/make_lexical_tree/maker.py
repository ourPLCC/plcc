from __future__ import annotations
from ...read_sections import Line
from .tree import LexicalTree
from .parser import parse
from .builder import LexicalTreeBuilder


def make_lexical_tree(lines: str|[str]|[Line]) -> LexicalTree:
    b = LexicalTreeBuilder()
    parse(b, lines)
    return b.result
