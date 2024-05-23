import re
from collections import Counter
from collections import defaultdict
from itertools import chain


from .bnfspec import BnfSpec
from .bnfspec import TntType


class BnfValidator:
    def validate(self, bnfspec):
        self.terminalNamesMustContainOnlyUppercaseAndUnderscore(bnfspec)
        # Invalid nonterminal names are detected by the parser
        self.altsMustBeUniqueAcrossLHS(bnfspec)
        self.duplicateLhsHaveAlternativeNames(bnfspec)
        self.altsMustBeUniqueWithinRule(bnfspec)
        self.duplicateRhsHaveAltExceptOne(bnfspec)
        self.nonRepeatingRulesCannotHaveSeparators(bnfspec)
        self.separatorsAreNonCapturingTerminals(bnfspec)
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

    def duplicateRhsHaveAltExceptOne(self, bnfspec):
        for rule in bnfspec.getRules():
            tntsByName = defaultdict(list)
            for t in rule.tnts:
                tntsByName[t.name].append(t)
            for name in tntsByName:
                if len(tntsByName[name]) > 1:
                    altCount = 0
                    for t in tntsByName[name]:
                        if t.alt:
                            altCount += 1
                    if altCount < len(tntsByName[name]) - 1:
                        raise self.SymbolNeedsFieldName(rule.line, name)

    class SymbolNeedsFieldName(Exception):
        def __init__(self, line, tntName):
            self.line = line
            self.tntName = tntName

    def nonRepeatingRulesCannotHaveSeparators(self, bnfspec):
        for rule in bnfspec.getRules():
            if rule.op != '**=' and rule.sep:
                raise self.NonRepeatingRulesCannotHaveSeparators(rule.line)

    class NonRepeatingRulesCannotHaveSeparators(Exception):
        def __init__(self, line):
            self.line = line

    def separatorsAreNonCapturingTerminals(self, bnfspec):
        for rule in bnfspec.getRules():
            if rule.sep and (rule.sep.type != TntType.TERMINAL or rule.sep.capture):
                raise self.SeparatorMustBeNonCapturingTerminal(rule.line)

    class SeparatorMustBeNonCapturingTerminal(Exception):
        def __init__(self, line):
            self.line = line

    def everyNonterminalAppearsOnLhs(self, bnfspec):
        lhsNames = set()
        for r in bnfspec.getRules():
            lhsNames.add(r.lhs.name)

        for r in bnfspec.getRules():
            for t in r.tnts:
                if t.type == TntType.NONTERMINAL:
                    if t.name not in lhsNames:
                        raise self.NonterminalMustAppearOnLHS(r.line, t.name)

    class NonterminalMustAppearOnLHS(Exception):
        def __init__(self, line, name):
            self.line = line
            self.name = name
