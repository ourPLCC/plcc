import re
from collections import Counter
from itertools import chain

from .bnfrule import TntType


class BnfValidator:
    def validate(self, bnfrules):
        self.terminalsHaveValidNames(bnfrules)
        self.nonterminalsHaveValidNames(bnfrules)
        self.lhsHaveDistinctAlternativeNames(bnfrules)
        self.duplicateLhsHaveAlternativeNames(bnfrules)
        self.rhsHaveDistinctAlternativeNamesWithinRule(bnfrules)
        self.duplicateRhsHaveAlternativeNames(bnfrules)
        self.onlyRepeatingRulesHaveSeparators(bnfrules)
        self.separatorsAreNoncapturingNonterminals(bnfrules)

    def terminalsHaveValidNames(self, bnfrules):
        validTerminalName = re.compile(r'^[A-Z_]+$')
        for r in bnfrules:
            for t in (t for t in r.tnts if t.type == TntType.TERMINAL):
                if not validTerminalName.match(t.name):
                    raise InvalidTerminalName(r.line, t.name)
            sep = r.sep
            if sep:
                if not validTerminalName.match(sep.name):
                    raise InvalidTerminalName(r.line, sep.name)

    class InvalidTerminalName(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def nonterminalsHaveValidNames(self, bnfrules):
        validNonterminalName = re.compile(r'^\w+$')
        for r in bnfrules:
            lhs = r.lhs
            if not validNonterminalName.match(lhs.name):
                raise InvalidNonterminalName(r.line, lhs.name)
            for t in (t for t in r.tnts if t.type == TntType.NONTERMINAL):
                if not validNonterminalName.match(t.name):
                    raise InvalidNonterminalName(r.line, t.name)

    class InvalidNonterminalName(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def lhsHaveDistinctAlternativeNames(bnfrules):
        ...

    def duplicateLhsHaveAlternativeNames(bnfrules):
        ...

    def rhsHaveDistinctAlternativeNamesWithinRule(bnfrules):
        ...

    def duplicateRhsHaveAlternativeNames(bnfrules):
        ...

    def onlyRepeatingRulesHaveSeparators(bnfrules):
        ...

    def separatorsAreNoncapturingNonterminals(bnfrules):
        ...

