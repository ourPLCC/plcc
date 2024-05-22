from dataclasses import dataclass
from .line import Line

@dataclass(frozen=True)
class LexRule:
    type: str
    name: str
    pattern: str
    quote: str
    end: str
    line: Line
