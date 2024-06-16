from pathlib import Path
from ..mark_blocks import BlockMarkingLineReader, isInBlock


class IncludeReader:
    def __init__(self, Reader=BlockMarkingLineReader, disableInclude=isInBlock):
        '''
        Reader:
            Reader() returns a reader. Readers have a read(file) method
            that returns a list of Lines. Defaults to BlockMarkingLineReader.

        disableInclude:
            disableInclude(line) returns True only if line should NOT be
            processed for include. Defaults to isInBlock.
        '''
        self.Reader = Reader
        self.disableInclude = disableInclude
        self.seen = []

    def read(self, file):
        p = Path(file)
        if not p.is_absolute():
            p = p.resolve()
        self.seen.append(p)
        lines = []
        for line in self.Reader().read(file):
            if not self.disableInclude(line) and line.string.startswith('%include '):
                includeFile = self.getFileToInclude(line.string)
                if includeFile in self.seen:
                    raise CircularIncludeError(line)
                lines.extend(self.read(includeFile))
            else:
                lines.append(line)
        self.seen.pop()
        return lines

    def getFileToInclude(self, string):
        p = Path(string.removeprefix('%include ').strip())
        if p.is_absolute():
            return p
        root = self.seen[-1].parent
        p = (root/p).resolve()
        return p


class CircularIncludeError(Exception):
    def __init__(self, line):
        self.line = line
