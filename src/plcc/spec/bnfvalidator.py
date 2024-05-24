import re
from collections import Counter
from collections import defaultdict
from itertools import chain


from .bnfspec import BnfSpec


class BnfValidator:
    def validate(self, bnfspec):
        # Invalid nonterminal names are detected by the parser
        self.terminalNamesMustContainOnlyUppercaseAndUnderscore(bnfspec)
        self.altsMustBeUniqueAcrossLHS(bnfspec)
        self.duplicateLhsHaveAlternativeNames(bnfspec)
        self.altsMustBeUniqueWithinRule(bnfspec)
        self.duplicateRhsHaveAltExceptOne(bnfspec)
        self.nonRepeatingRulesCannotHaveSeparators(bnfspec)
        self.separatorsAreNonCapturing(bnfspec)
        self.everyNonterminalAppearsOnLhs(bnfspec)

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
        seen = set()
        for r in bnfspec.getRules():
            if r.lhs.alt and r.lhs.alt in seen:
                raise self.DuplicateConcreteClassNameInLhs(r.line, r.lhs.alt)
            seen.add(r.lhs.alt)

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
            if rule.getDuplicateRhsAlts():
                raise self.FieldNamesMustBeUniqueWithinRule(rule.line)

    class FieldNamesMustBeUniqueWithinRule(Exception):
        def __init__(self, line):
            self.line = line

    def duplicateRhsHaveAltExceptOne(self, bnfspec):
        for rule in bnfspec.getRules():
            dupTntsByName = rule.getDuplicateTntsGroupedByName()
            for name in dupTntsByName:
                dups = dupTntsByName[name]
                altCount = sum(1 for t in dups if t.alt)
                if altCount < len(dups) - 1:
                    raise self.SymbolNeedsFieldName(rule.line, name)

    class SymbolNeedsFieldName(Exception):
        def __init__(self, line, tntName):
            self.line = line
            self.tntName = tntName

    def nonRepeatingRulesCannotHaveSeparators(self, bnfspec):
        for rule in bnfspec.getNonrepeatingRules():
            if rule.sep:
                raise self.NonRepeatingRulesCannotHaveSeparators(rule.line)

    class NonRepeatingRulesCannotHaveSeparators(Exception):
        def __init__(self, line):
            self.line = line

    def separatorsAreNonCapturing(self, bnfspec):
        for rule in bnfspec.getRulesThatHaveSep():
            if rule.sep.isCapture:
                raise self.SeparatorMustBeNonCapturing(rule.line)

    class SeparatorMustBeNonCapturing(Exception):
        def __init__(self, line):
            self.line = line

    def everyNonterminalAppearsOnLhs(self, bnfspec):
        lhsNames = bnfspec.getLhsNames()
        for r, t in bnfspec.getRhsNonterminals():
            if t.name not in lhsNames:
                raise self.NonterminalMustAppearOnLHS(r.line, t.name)

    class NonterminalMustAppearOnLHS(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name
