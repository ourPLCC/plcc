import pathlib


from .lines import Line


class File:
    def __init__(self, path):
        self._path = path
        self._lines = self._readLines(path)

    def _readLines(self, path):
        with pathlib.Path(path).open(mode='r') as file:
            for number, line in enumerate(file, start=1):
                string = line.rstrip()
                yield Line(path=path, number=number, string=string)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._lines)

    def getPath(self):
        return self._path
