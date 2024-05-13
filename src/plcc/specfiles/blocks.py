from typing import Iterator, Optional, Iterable


from .files import File
from .lines import Line


class BlockMarker(Iterable[Line]):
    def __init__(self, file: File, brackets: Optional[dict[str,str]] = None):
        if brackets is not None:
            self._brackets = brackets
        else:
            self._brackets = {
                '%%%': '%%%',
                '%%{': '%%}'
            }
        self._file = file
        self._isInBlock = False
        self._closing = ''

    def __iter__(self) -> Iterator[Line]:
        return self

    def __next__(self) -> Line:
        line = next(self._file)
        if not self._isInBlock and line.string in self._brackets:
            self._isInBlock = True
            self._closing = self._brackets[line.string]
        elif self._isInBlock and line.string == self._closing:
            self._isInBlock = False
        elif self._isInBlock:
            line = line.markIsInBlock()
        return line

    def getPath(self) -> str:
        return self._file.getPath()
