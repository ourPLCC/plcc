from __future__ import annotations


from .builder import BlocksBuilder
from .parser import parse
from .block import Line, Block


def make_blocks(lines: [Line]) -> [Line|Block]:
    b = BlocksBuilder()
    parse(b, lines)
    return b.getContent()
