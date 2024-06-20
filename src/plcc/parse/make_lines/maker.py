from __future__ import annotations


from .builder import LinesBuilder
from .parser import parse
from .line import Line


def make_lines(strings: str|[str], file: str = None) -> [Line]:
    b = LinesBuilder()
    parse(b, strings, file)
    return b.getLines()
