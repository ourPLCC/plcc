from ..read_lines import LineReader
from . import BlockMarker


class BlockMarkingLineReader:
    def read(self, file):
        lines = LineReader().read(file)
        return BlockMarker().mark(lines)
