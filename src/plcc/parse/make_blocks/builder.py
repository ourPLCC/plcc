from overrides import override


from .parser import Builder
from .block import Block, Line


class BlocksBuilder(Builder):
    @override
    def begin(self) -> None:
        self.content = []
        self.openLine = None
        self.block = None

    @override
    def open(self, line: Line) -> None:
        if self.openLine:
            raise NestedBlockError(line)
        self.openLine = line
        self.block = []

    @override
    def close(self, line: Line) -> None:
        if not self.openLine:
            raise ClosingUnopenedBlockError(line)
        b = Block(open=self.openLine, close=line, lines=self.block)
        self.content.append(b)
        self.openLine = None
        self.block = None

    @override
    def line(self, line: Line) -> None:
        if self.openLine:
            self.block.append(line)
        else:
            self.content.append(line)

    @override
    def end(self) -> None:
        if self.openLine:
            raise UnclosedBlockError(self.openLine)

    def getContent(self) -> [Line|Block]:
        return self.content


class NestedBlockError(Exception):
    def __init__(self, line):
        self.line = line


class ClosingUnopenedBlockError(Exception):
    def __init__(self, line):
        self.line = line
