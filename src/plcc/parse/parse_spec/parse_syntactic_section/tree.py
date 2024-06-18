from dataclasses import dataclass


@dataclass(frozen=True)
class SyntacticTree:
    rules: [RepeatingRule|StandardRule]


@dataclass(frozen=True)
class RepeatingRule:
    nonterminal: Defining
    symbols: [Capturing|NonCapturing]
    separator: Terminal


@dataclass(frozen=True)
class StandardRule:
    nonterminal: Defining
    symbols: [Capturing|NonCapturing]


@dataclass(frozen=True)
class Defining:
    sybmol: Nonterminal
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
class NonCapturing:
    symbol: Terminal|Nonterminal
    line: Line
    column: int


@dataclass(frozen=True)
class Capturing:
    symbol: Terminal|Nonterminal
    disambiguation: str
    line: Line
    column: int
