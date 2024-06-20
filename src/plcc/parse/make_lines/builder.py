from overrides import override


from .parser import Builder
from .line import Line


class LinesBuilder(Builder):
    @override
    def begin(self) -> None:
        self.lines = []
        self.file = None

    @override
    def setFile(self, file: str) -> None:
        self.file = file

    @override
    def line(self, string: str, number: int) -> None:
        self.lines.append(Line(string, number, self.file))

    @override
    def end(self) -> None:
        pass

    def getLines(self):
        return self.lines
