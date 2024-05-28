import re
from collections import Counter
from collections import defaultdict
from itertools import chain


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
            if r.leftHandSymbol.alt and r.leftHandSymbol.alt in seen:
                raise self.DuplicateConcreteClassNameInLhs(r.line, r.leftHandSymbol.alt)
            seen.add(r.leftHandSymbol.alt)

    class DuplicateConcreteClassNameInLhs(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def duplicateLhsHaveAlternativeNames(self, bnfspec):
        for rule in bnfspec.getRulesWithDuplicateLhsNames():
            if not rule.leftHandSymbol.alt:
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
            symbolsByName = rule.getDuplicateRightHandSymbolsGroupedByName()
            for name in symbolsByName:
                duplicates = symbolsByName[name]
                altCount = sum(1 for t in duplicates if t.alt)
                if altCount < len(duplicates) - 1:
                    raise self.SymbolNeedsFieldName(rule.line, name)

    class SymbolNeedsFieldName(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def nonRepeatingRulesCannotHaveSeparators(self, bnfspec):
        for rule in bnfspec.getNonrepeatingRules():
            if rule.separator:
                raise self.NonRepeatingRulesCannotHaveSeparators(rule.line)

    class NonRepeatingRulesCannotHaveSeparators(Exception):
        def __init__(self, line):
            self.line = line

    def separatorsAreNonCapturing(self, bnfspec):
        for rule in bnfspec.getRulesThatHaveSep():
            if rule.separator.isCapture:
                raise self.SeparatorMustBeNonCapturing(rule.line)

    class SeparatorMustBeNonCapturing(Exception):
        def __init__(self, line):
            self.line = line

    def everyNonterminalAppearsOnLhs(self, bnfspec):
        lhsNames = bnfspec.getLhsNames()
        for rule, symbol in bnfspec.getRhsNonterminals():
            if symbol.name not in lhsNames:
                raise self.NonterminalMustAppearOnLHS(rule.line, symbol.name)

    class NonterminalMustAppearOnLHS(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name
