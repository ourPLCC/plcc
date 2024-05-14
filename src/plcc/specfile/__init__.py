from __future__ import annotations
import pathlib
from typing import Iterator, Iterable
import gettext


_ = gettext.gettext


from .line import Line
from .file import File
from .block import BlockMarker
from .include import Includer, CircularIncludeException


def specfile(path: str) -> SpecFile:
    return SpecFile(
                path,
                brackets = {
                    '%%%': '%%%',
                    '%%{': '%%}'
                },
                includePattern = r'^%include\s+(.+)(#.*)?'
            )

class SpecFile(Iterable[Line]):
    def __init__(self,
                pathString: str,
                brackets: dict[str,str],
                includePattern: str):
        self._validate_pathString(pathString)
        pathString = str(pathlib.Path(pathString).resolve())
        file = File(pathString)
        blockMarker = BlockMarker(file, brackets)
        includer = Includer(blockMarker, includePattern)
        self._lines = includer

    def _validate_pathString(self, pathString: str) -> None:
        self._must_be_a_str(pathString)
        self._must_contain_a_non_whitespace(pathString)

    def _must_be_a_str(self, x: str) -> None:
        if not isinstance(x, str):
            raise TypeError(_('Must be a str.'))

    def _must_contain_a_non_whitespace(self, x: str) -> None:
        if x.strip() == '':
            raise ValueError(_('Must contain a non-whitespace.'))

    def __iter__(self) -> Iterator[Line]:
        return self

    def __next__(self) -> Line:
        return next(self._lines)
