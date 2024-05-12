import pathlib


from .files import File
from .blocks import BlockMarker
from .includes import Includer, CircularIncludeException


class SpecFile:
    def __init__(self, pathString):
        self._validate_pathString(pathString)
        pathString = str(pathlib.Path(pathString).resolve())
        file = File(pathString)
        blockMarker = BlockMarker(file)
        includer = Includer(blockMarker)
        self._lines = includer

    def _validate_pathString(self, pathString):
        self._must_be_a_str(pathString)
        self._must_contain_a_non_whitespace(pathString)

    def _must_be_a_str(self, x):
        if not isinstance(x, str):
            raise TypeError('Must be a str.')

    def _must_contain_a_non_whitespace(self, x):
        if x.strip() == '':
            raise ValueError('Must contain a non-whitespace.')

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._lines)
