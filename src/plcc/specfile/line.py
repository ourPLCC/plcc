from __future__ import annotations
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Line:
    path: str
    number: int
    string: str
    isInBlock: bool = False

    def markIsInBlock(self) -> Line:
        return replace(self, isInBlock=True)


def toLines(string):
    path='__str__'
    for i, s in enumerate(string.splitlines(), start=1):
        yield Line(path, i, s, isInBlock=False)
