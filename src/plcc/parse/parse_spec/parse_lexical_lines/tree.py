from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class LexicalTree:
    rules: [TokenRule|SkipRule]


@dataclass(frozen=True)
class TokenRule:
    name: str
    pattern: str
    line: Line


@dataclass(frozen=True)
class SkipRule:
    name: str
    pattern: str
    line: Line
