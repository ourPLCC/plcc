from .line_in_block import markLineInBlock


class BlockMarker:
    def __init__(self):
        self.isInBlock = False
        self.unclosedLineInBlock = None
        self.brackets = {
            '%%%': '%%%',
            '%%{': '%%}',
        }
        self.close = None

    def mark(self, lines):
        marked = [self.maybeMarkLine(line) for line in lines]
        if self.unclosedLineInBlock:
            raise UnclosedBlockError(self.unclosedLineInBlock)
        return marked

    def maybeMarkLine(self, line):
        if not self.isInBlock and line.string in self.brackets:
            self.startBlock(line)
            return line
        elif self.isInBlock and line.string == self.close:
            self.endBlock()
            return line
        elif self.isInBlock:
            return markLineInBlock(line)
        else:
            return line

    def startBlock(self, line):
        self.isInBlock = True
        self.unclosedLineInBlock = line
        self.close = self.brackets[line.string]

    def endBlock(self):
        self.isInBlock = False
        self.unclosedLineInBlock = None
        self.close = None


class UnclosedBlockError(Exception):
    def __init__(self, unclosedBlockStartLine):
        self.unclosedBlockStartLine = unclosedBlockStartLine
