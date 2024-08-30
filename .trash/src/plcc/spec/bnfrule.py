from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum
from collections import defaultdict
from collections import Counter


from .line import Line
from .symbol import Symbol


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

    def getDuplicateRhsGivenNames(self):
        counts = Counter(self.getGivenNames())
        duplicates = set()
        for givenName in counts:
            if counts[givenName] > 1:
                duplicates.add(givenName)
        return duplicates

    def getGivenNames(self):
        for symbol in self.rightHandSymbols:
            if symbol.givenName:
                yield symbol.givenName
