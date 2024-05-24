from __future__ import annotations
from dataclasses import dataclass, replace
from enum import Enum
from collections import defaultdict
from collections import Counter


from .line import Line


@dataclass(frozen=True)
class BnfRule:
    line: Line
    lhs: Tnt
    tnts: List[Tnt]
    isRepeating: bool = False
    sep: Tnt = None

    def getTntsByName(self):
        tntsByName = defaultdict(list)
        for t in self.tnts:
            tntsByName[t.name].append(t)
        return tntsByName

    def getDuplicateTntsGroupedByName(self):
        tntsByName = self.getTntsByName()
        toD = set(name for name in tntsByName if len(tntsByName[name]) <= 1)
        for name in toD:
            del tntsByName[name]
        return tntsByName

    def getDuplicateRhsAlts(self):
        c = Counter(self.getAlts())
        dups = set()
        for alt in c:
            if c[alt] > 1:
                dups.add(alt)
        return dups

    def getAlts(self):
        for t in self.tnts:
            if t.alt:
                yield t.alt


@dataclass(frozen=True)
class Tnt:
    name: str
    alt: str
    isCapture: bool
    isTerminal: bool = False
