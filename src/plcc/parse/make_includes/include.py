from __future__ import annotations
from dataclasses import dataclass
from ..make_blocks import Line


@dataclass(frozen=True)
class Include:
    file: str
    line: Line
