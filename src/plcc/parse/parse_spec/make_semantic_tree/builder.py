from __future__ import annotations
from overrides import override


from .parser import Builder


from .tree import SemanticTree, Block
from ...read_sections import Line


class SemanticTreeBuilder(Builder):
    @override
    def begin(self):
        self.result = None
        self.block_header = None
        self.blocks = []

    @override
    def startBlock(self, module:str, location:str, line: Line) -> None:
        if self.block_header is not None:
            raise MultipleBlockHeaderError(line)
        self.block_header = (module, location, line)

    @override
    def setCode(self, lines: List[Line]) -> None:
        if self.block_header is None:
            raise BlockMissingHeaderError(line)
        module, location, line = self.block_header
        self.block_header = None
        self.blocks.append(Block(module=module,location=location,code=lines, line=line))

    @override
    def end(self):
        self.result = SemanticTree(blocks=self.blocks)


class MultipleBlockHeaderError(Exception):
    def __init__(self, line):
        self.line = line


class BlockMissingHeaderError(Exception):
    def __init__(self, line):
        self.line = line
