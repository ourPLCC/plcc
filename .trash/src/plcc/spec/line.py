from __future__ import annotations
from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Line:
    path: str
    number: int
    string: str
    isInCodeBlock: bool = False

    def markInCodeBlock(self) -> Line:
        return replace(self, isInCodeBlock=True)

