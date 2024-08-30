from __future__ import annotations
from dataclasses import dataclass


from ..make_lines import Line


@dataclass(frozen=True)
class Block:
    open: Line
    close: Line
    lines: [Line]
