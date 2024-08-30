import re
from collections import Counter
from collections import defaultdict
from itertools import chain


class BnfValidator:
    def validate(self, bnfspec):
        # Invalid nonterminal names are detected by the parser
        self.terminalNamesMustContainOnlyUppercaseAndUnderscore(bnfspec)
        self.givenNamesMustBeUniqueAcrossLHS(bnfspec)
        self.duplicateLhsHaveGivenNames(bnfspec)
        self.givenNamesMustBeUniqueWithinRule(bnfspec)
        self.duplicateRhsHaveGivenNameExceptOne(bnfspec)
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

    def givenNamesMustBeUniqueAcrossLHS(self, bnfspec):
        seen = set()
        for r in bnfspec.getRules():
            if r.leftHandSymbol.givenName and r.leftHandSymbol.givenName in seen:
                raise self.DuplicateConcreteClassNameInLhs(r.line, r.leftHandSymbol.givenName)
            seen.add(r.leftHandSymbol.givenName)

    class DuplicateConcreteClassNameInLhs(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name

    def duplicateLhsHaveGivenNames(self, bnfspec):
        for rule in bnfspec.getRulesWithDuplicateLhsNames():
            if not rule.leftHandSymbol.givenName:
                raise self.DuplicateLhsMustProvideConcreteClassName(rule.line)

    class DuplicateLhsMustProvideConcreteClassName(Exception):
        def __init__(self, line):
            self.line = line

    def givenNamesMustBeUniqueWithinRule(self, bnfspec):
        for rule in bnfspec.getRules():
            if rule.getDuplicateRhsGivenNames():
                raise self.FieldNamesMustBeUniqueWithinRule(rule.line)

    class FieldNamesMustBeUniqueWithinRule(Exception):
        def __init__(self, line):
            self.line = line

    def duplicateRhsHaveGivenNameExceptOne(self, bnfspec):
        for rule in bnfspec.getRules():
            symbolsByName = rule.getDuplicateRightHandSymbolsGroupedByName()
            for name in symbolsByName:
                duplicates = symbolsByName[name]
                givenNameCount = sum(1 for t in duplicates if t.givenName)
                if givenNameCount < len(duplicates) - 1:
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
