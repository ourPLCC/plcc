from dataclasses import dataclass
import re


from .lines import Line


@dataclass
class Block:
    lines: [Line]


def parse_blocks(lines, brackets=None, Block=Block):
    if lines is None:
        return []
    if brackets is None:
        PPP = re.compile(r'^%%%(?:\s*#.*)?$')
        PPLC = re.compile(r'^%%{(?:\s*#.*)?$')
        PPRC = re.compile(r'^%%}(?:\s*#.*)?$')
        brackets = {
            PPP: PPP,
            PPLC: PPRC
        }
    return BlockParser(brackets, Block).parse(lines)


class UnclosedBlockError(Exception):
    def __init__(self, line):
        self.line = line


class BlockParser():
    def __init__(self, brackets, Block):
        self.Block = Block
        self.brackets = brackets
        self.closing = None

    def parse(self, lines):
        self.lines = iter(lines)
        for line in self.lines:
            if not self.isBlockStart(line):
                yield line
            else:
                yield from self.parseBlock(line)

    def isBlockStart(self, line):
        for b in self.brackets:
            if b.match(line.string):
                return True
        return False

    def parseBlock(self, line):
        blockLines = [line]
        self.setClosingFor(line)
        for line in self.lines:
            blockLines.append(line)
            if self.isClosing(line):
                yield self.Block(blockLines)
                return
        raise UnclosedBlockError(line)

    def setClosingFor(self, line):
        for b in self.brackets:
            if b.match(line.string):
                self.closing = self.brackets[b]
                return

    def isClosing(self, line):
        return self.closing.match(line.string) is not None
