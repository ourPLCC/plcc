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

