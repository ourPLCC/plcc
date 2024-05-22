from __future__ import annotations
from dataclasses import dataclass
from .line import Line


@dataclass
class BnfRule:
    lhs: Tnt
    op: str
    tnts: List[Tnt]
    sep: Tnt = None


@dataclass(frozen=True)
class Tnt:
    type: str
    name: str
    alt: str
    capture: bool
