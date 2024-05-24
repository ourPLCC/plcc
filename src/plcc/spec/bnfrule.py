from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum
from collections import defaultdict
from collections import Counter


from .line import Line


@dataclass(frozen=True)
class BnfRule:
    line: Line
    leftHandSymbol: Symbol
    rightHandSymbols: List[Symbol]
    isRepeating: bool = False
    separator: Symbol = None

    def getRightHandSymbolsByName(self):
        symbolsByName = defaultdict(list)
        for symbol in self.rightHandSymbols:
            symbolsByName[symbol.name].append(symbol)
        return symbolsByName

    def getDuplicateRightHandSymbolsGroupedByName(self):
        symbolsByName = self.getRightHandSymbolsByName()
        toDelete = set(name for name in symbolsByName if len(symbolsByName[name]) <= 1)
        for name in toDelete:
            del symbolsByName[name]
        return symbolsByName

    def getDuplicateRhsAlts(self):
        counts = Counter(self.getAlts())
        duplicates = set()
        for alt in counts:
            if counts[alt] > 1:
                duplicates.add(alt)
        return duplicates

    def getAlts(self):
        for symbol in self.rightHandSymbols:
            if symbol.alt:
                yield symbol.alt


@dataclass(frozen=True)
class Symbol:
    name: str
    alt: str
    isCapture: bool
    isTerminal: bool = False
