from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class SyntacticTree:
    rules: [RepeatingRule|StandardRule]


@dataclass
class RepeatingRule:
    defined: Defined
    symbols: [Captured|Uncaptured]
    separator: Terminal


@dataclass(frozen=True)
class StandardRule:
    defined: Defined
    symbols: [Captured|Uncaptured]


@dataclass(frozen=True)
class Defined:
    symbol: Nonterminal
    disambiguation: str
    line: Line
    column: int


@dataclass(frozen=True)
class Terminal:
    name: str


@dataclass(frozen=True)
class Nonterminal:
    name: str


@dataclass(frozen=True)
class Uncaptured:
    symbol: Terminal|Nonterminal
    line: Line
    column: int


@dataclass(frozen=True)
class Captured:
    symbol: Terminal|Nonterminal
    disambiguation: str
    line: Line
    column: int
