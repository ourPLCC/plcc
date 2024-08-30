from overrides import override


from .parser import Builder
from .line import Line


class LinesBuilder(Builder):
    @override
    def begin(self) -> None:
        self.lines = []
        self.file = None
        self.number = 1

    @override
    def setFile(self, file: str) -> None:
        self.file = file

    @override
    def line(self, string: str) -> None:
        self.lines.append(Line(string, self.number, self.file))
        self.number += 1

    @override
    def end(self) -> None:
        pass

    def getLines(self):
        return self.lines
