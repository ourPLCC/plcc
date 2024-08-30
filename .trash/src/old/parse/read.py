from .line import Line


def readSpecLines(specPath):
    return SpecReader().readLines(specPath)


class SpecReader():
    def __init__(self):
        self._path = None
        self._seenStack = []
        self._inCodeBlock = False

    def readLines(self, path):
        self._path = path
        self._seenStack.append(self._path)
        yield from self._readLines(self._path)

    def _readLines(self, filePath):
        with open(filePath) as f:
            line_number = 1
            for line in f:
                line = line.rstrip()
                if self._isInclude(line):
                    yield from self._include(line)
                elif self._isOpenCodeBlock(line):
                    self._openCodeBlock()
                elif self._isCloseCodeBlock(line):
                    self._closeCodeBlock()
                else:
                    yield Line(filePath, line_number, line)
                    line_number += 1

    def _isInclude(self, line):
        return not self._inCodeBlock and line.startswith('%include ')

    def _include(self, line):
        file = line.removeprefix('%include ')
        if file in self._seenStack:
            raise Exception(f'Circular %include detected: {file}')
        self._seenStack.append(file)
        yield from self._readLines(file)
        self._seenStack.pop()

    def _isOpenCodeBlock(self, line):
        return not self._inCodeBlock and line in ['%%%', '%%{']

    def _isCloseCodeBlock(self, line):
        return self._inCodeBlock and line in ['%%%', '%%}']

    def _openCodeBlock(self):
        self._inCodeBlock = True

    def _closeCodeBlock(self):
        self._inCodeBlock = False
