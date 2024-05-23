import re
from collections import Counter
from itertools import chain


from .bnfspec import BnfSpec


class BnfValidator:
    def validate(self, bnfspec):
        self.terminalNamesMustContainOnlyUppercaseAndUnderscore(bnfspec)
        # Invalid nonterminal names are detected by the parser
        self.altsMustBeUniqueAcrossLHS(bnfspec)
        self.duplicateLhsHaveAlternativeNames(bnfspec)
        self.altsMustBeUniqueWithinRule(bnfspec)
        # self.duplicateRhsHaveAlternativeNames(bnfspec)
        # self.onlyRepeatingRulesHaveSeparators(bnfspec)
        # self.separatorsAreNoncapturingNonterminals(bnfspec)
        # self.everyNonterminalAppearsOnLhs(bnfspec)

    def terminalNamesMustContainOnlyUppercaseAndUnderscore(self, bnfspec):
        validTerminalName = re.compile(r'^[A-Z_]+$')
        for rule, t in bnfspec.getTerminals():
            if not validTerminalName.match(t.name):
                raise self.InvalidTerminalName(rule.line, t.name)

    class InvalidTerminalName(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def altsMustBeUniqueAcrossLHS(self, bnfspec):
        names = set()
        for r in bnfspec.getRules():
            if r.lhs.alt and r.lhs.alt in names:
                raise self.DuplicateConcreteClassNameInLhs(r.line, r.lhs.alt)
            names.add(r.lhs.alt)

    class DuplicateConcreteClassNameInLhs(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def duplicateLhsHaveAlternativeNames(self, bnfspec):
        for rule in bnfspec.getRulesWithDuplicateLhsNames():
            if not rule.lhs.alt:
                raise self.DuplicateLhsMustProvideConcreteClassName(rule.line)

    class DuplicateLhsMustProvideConcreteClassName(Exception):
        def __init__(self, line):
            self.line = line

    def altsMustBeUniqueWithinRule(self, bnfspec):
        for rule in bnfspec.getRules():
            seen = set()
            for t in rule.tnts:
                if t.alt:
                    if t.alt in seen:
                        raise self.FieldNamesMustBeUniqueWithinRule(rule.line)
                    seen.add(t.alt)

    class FieldNamesMustBeUniqueWithinRule(Exception):
        def __init__(self, line):
            self.line = line

    # def duplicateRhsHaveAlternativeNames(bnfspec):
    #     ...

    # def onlyRepeatingRulesHaveSeparators(bnfspec):
    #     ...

    # def separatorsAreNoncapturingNonterminals(bnfspec):
    #     ...

