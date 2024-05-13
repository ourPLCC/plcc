import pathlib
import re
from typing import Iterable, Iterator


from .blocks import BlockMarker
from .files import File
from .lines import Line


class Includer(Iterable[Line]):
    def __init__(self, blockMarker: BlockMarker, includePattern: str = r'^%include\s+(.+)(#.*)?'):
        self._includePattern = includePattern
        self._includeStack = [blockMarker.getPath()]
        self._lines = self._readLines(blockMarker)

    def _readLines(self, file: Iterator[Line]) -> Iterator[Line]:
        for line in file:
            m = re.match(self._includePattern, line.string)
            if not line.isInBlock and m:
                yield from self._processInclude(line, m.group(1))
            else:
                yield line

    def _processInclude(self, sourceLine: Line, includePath: str) -> Iterator[Line]:
        includePath = self._resolve_includePath(sourceLine.path, includePath)
        self._check_for_circular_include(sourceLine, includePath)
        yield from self._includeFile(includePath)

    def _resolve_includePath(self, source: str, include: str) -> str:
        sourcePath = pathlib.Path(source)
        includePath = pathlib.Path(include)
        if not includePath.is_absolute():
            includePath = (sourcePath.parent / includePath).resolve()
        return str(includePath)

    def _check_for_circular_include(self, sourceLine: Line, includePath: str) -> None:
        if includePath in self._includeStack:
            raise CircularIncludeException(f'{str(sourceLine)}')

    def _includeFile(self, includePath: str) -> Iterator[Line]:
        self._includeStack.append(includePath)
        yield from self._readLines(BlockMarker(File(includePath)))
        self._includeStack.pop()

    def __iter__(self) -> Iterator[Line]:
        return self

    def __next__(self) -> Line:
        return next(self._lines)


class CircularIncludeException(Exception):
    ...
