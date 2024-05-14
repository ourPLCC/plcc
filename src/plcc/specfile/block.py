from __future__ import annotations
from typing import Iterator, Optional, Iterable


from .file import File
from .line import Line


class BlockMarker(Iterable[Line]):
    def __init__(self, file: File, brackets: dict[str,str]):
        self._brackets = brackets
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

    def new(self, file: File) -> BlockMarker:
        return type(self)(file, self._brackets)
