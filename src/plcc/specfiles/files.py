import pathlib
from typing import Iterator, Iterable


from .lines import Line


class File:
    def __init__(self, path: str):
        self._path: str = path
        self._lines: Iterator[Line] = self._readLines(path)

    def _readLines(self, path: str) -> Iterator[Line]:
        with pathlib.Path(path).open(mode='r') as file:
            for number, line in enumerate(file, start=1):
                string = line.rstrip()
                yield Line(path=path, number=number, string=string)

    def __iter__(self) -> Iterator[Line]:
        return self

    def __next__(self) -> Line:
        return next(self._lines)

    def getPath(self) -> str:
        return self._path
