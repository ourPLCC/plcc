from dataclasses import dataclass, replace
from .line import Line


@dataclass(frozen=True)
class LexRule:
    line: Line
    name: str
    pattern: str
    remainder: str
    isToken: bool = True
