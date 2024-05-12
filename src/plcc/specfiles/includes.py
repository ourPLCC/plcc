import pathlib
import re


from .blocks import BlockMarker
from .files import File


class Includer:
    def __init__(self, blockMarker, includePattern=r'^%include\s+(.+)(#.*)?'):
        self._includePattern = includePattern
        self._includeStack = [blockMarker.getPath()]
        self._lines = self._readLines(blockMarker)

    def _readLines(self, file):
        for line in file:
            m = re.match(self._includePattern, line.string)
            print(f'{line=} {m=}')
            if self._isInclude(line, m):
                yield from self._processInclude(line, m.group(1))
            else:
                yield line

    def _isInclude(self, line, isInclude):
        return not line.isInBlock and isInclude

    def _processInclude(self, sourceLine, includePath):
        includePath = self._resolve_includePath(sourceLine, includePath)
        self._check_for_circular_include(sourceLine, includePath)
        yield from self._includeFile(includePath)

    def _resolve_includePath(self, source, include):
        source = pathlib.Path(source.path)
        include = pathlib.Path(include)
        if not include.is_absolute():
            include = (source.parent / include).resolve()
        return str(include)

    def _check_for_circular_include(self, sourceLine, includePath):
        if str(includePath) in self._includeStack:
            raise CircularIncludeException(f'{str(sourceLine)}')

    def _includeFile(self, includePath):
        self._includeStack.append(includePath)
        yield from self._readLines(BlockMarker(File(includePath)))
        self._includeStack.pop()


    def __iter__(self):
        return self

    def __next__(self):
        return next(self._lines)


class CircularIncludeException(Exception):
    ...
