import re
from collections import Counter
from itertools import chain


from .bnfspec import BnfSpec


class BnfValidator:
    def validate(self, bnfspec):
        self.terminalNamesMustContainOnlyUppercaseAndUnderscore(bnfspec)
        # self.nonterminalsHaveValidNames(bnfspec)
        # self.lhsHaveDistinctAlternativeNames(bnfspec)
        # self.duplicateLhsHaveAlternativeNames(bnfspec)
        # self.rhsHaveDistinctAlternativeNamesWithinRule(bnfspec)
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

    # def nonterminalsHaveValidNames(self, bnfspec):
    #     validNonterminalName = re.compile(r'^\w+$')
    #     for rule, nt in bnfspec.getNonterminals():
    #         if not validNonterminalName.match(nt.name):
    #             raise self.InvalidNonterminalName(rule.name, nt.name)

    # class InvalidNonterminalName(Exception):
    #     def __init__(self, line, name):
    #         self.line = line
    #         self.name = name

    # def lhsHaveDistinctAlternativeNames(bnfspec):
    #     names = set()
    #     for r in bnfspec.getRules():
    #         if r.lhs.alt and r.lhs.alt in names:
    #             raise self.DuplicateLhsAlternateName(r.line, r.lhs.alt)
    #         names.add(r.lhs.alt)

    # class DuplicateLhsAlternateName(Exception):
    #     def __init__(self, line, name):
    #         self.line = line
    #         self.name = name

    # def duplicateLhsHaveAlternativeNames(bnfspec):
    #     for rule in bnfspec.getRulesWithDuplicateLhsNames():
    #         if not rule.lhs.alt:
    #             raise self.LhsMissingAlternativeName(rule.line)

    # class LhsMissingAlternativeName(Exception):
    #     def __init__(self, line):
    #         self.line = line

    # def rhsHaveDistinctAlternativeNamesWithinRule(bnfspec):
    #     ...

    # def duplicateRhsHaveAlternativeNames(bnfspec):
    #     ...

    # def onlyRepeatingRulesHaveSeparators(bnfspec):
    #     ...

    # def separatorsAreNoncapturingNonterminals(bnfspec):
    #     ...

