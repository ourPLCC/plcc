from .files import File


class BlockMarker:
    def __init__(self, file, brackets=None):
        if not brackets:
            brackets = {
                '%%%': '%%%',
                '%%{': '%%}'
            }
        if isinstance(file, str):
            file = File(file)
        if not isinstance(file, File):
            raise TypeError
        self._brackets = brackets
        self._file = file
        self._isInBlock = False
        self._closing = None

    def __iter__(self):
        return self

    def __next__(self):
        line = next(self._file)
        if not self._isInBlock and line.string in self._brackets:
            self._isInBlock = True
            self._closing = self._brackets[line.string]
        elif self._isInBlock and line.string == self._closing:
            self._isInBlock = False
            self._closing = None
        elif self._isInBlock:
            line = line.markIsInBlock()
        return line

    def getPath(self):
        return self._file.getPath()
