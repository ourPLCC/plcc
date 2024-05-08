from dataclasses import dataclass


@dataclass
class Line:
    file: str
    line: int
    text: str
