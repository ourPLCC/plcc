from dataclasses import dataclass
from typing import List
from plcc.load_spec.load_rough_spec.parse_lines import Line


@dataclass(frozen=True)
class Symbol:
    name: str | None
    pass


@dataclass(frozen=True)
class Terminal(Symbol):
    pass


@dataclass(frozen=True)
class CapturingSymbol(Symbol):
    altName: str | None = None
    pass


@dataclass(frozen=True)
class CapturingTerminal(CapturingSymbol):
    pass


@dataclass(frozen=True)
class NonTerminal(CapturingSymbol):
    pass


@dataclass(frozen=True)
class LhsNonTerminal(NonTerminal):
    pass


@dataclass(frozen=True)
class RhsNonTerminal(NonTerminal):
    pass


@dataclass(frozen=True)
class SyntacticRule:
    line: Line
    lhs: LhsNonTerminal
    rhsSymbolList: List[Symbol]
    pass


@dataclass(frozen=True)
class StandardSyntacticRule(SyntacticRule):
    pass


@dataclass(frozen=True)
class RepeatingSyntacticRule(SyntacticRule):
    separator: Terminal | None = None
    pass


@dataclass
class SyntacticSpec(list):
    def __init__(self, rules=None):
        if rules: super(rules)
    pass


class MalformedLHSError(Exception):
    def __init__(self, line):
        self.line = line


class MalformedBNFError(Exception):
    def __init__(self, line):
        self.line = line
