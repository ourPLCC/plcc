from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    string: str
    number: int
    file: str
