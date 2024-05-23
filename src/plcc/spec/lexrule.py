from dataclasses import dataclass, replace
from .line import Line

@dataclass(frozen=True)
class LexRule:
    line: Line
    name: str
    pattern: str
    quote: str
    end: str
    isToken: bool = True

    def toSkip(self):
        return replace(self, isToken=False)
