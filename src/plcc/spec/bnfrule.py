from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from .line import Line


@dataclass
class BnfRule:
    line: Line
    lhs: Tnt
    op: str
    tnts: List[Tnt]
    sep: Tnt = None


@dataclass(frozen=True)
class Tnt:
    type: TntType
    name: str
    alt: str
    capture: bool


class TntType(Enum):
    TERMINAL=1
    NONTERMINAL=2
