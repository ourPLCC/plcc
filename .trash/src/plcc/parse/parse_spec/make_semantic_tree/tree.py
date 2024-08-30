from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class SemanticTree:
    blocks: [Block]


@dataclass(frozen=True)
class Block:
    module: str
    location: str
    code: [Line]
    line: Line
