from collections import defaultdict
from .bnfvalidator import BnfValidator


class BnfSpec:
    def __init__(self, bnfRules):
        self._bnfRules = bnfRules

    def validate(self):
        BnfValidator().validate(self)

    def getTerminals(self):
        for rule in self._bnfRules:
            for tnt in rule.rightHandSymbols:
                if tnt.isTerminal:
                    yield rule, tnt
            if rule.separator:
                yield rule, rule.separator

    def getRules(self):
        for rule in self._bnfRules:
            yield rule

    def getRulesWithDuplicateLhsNames(self):
        rulesByLhsName = defaultdict(list)
        for r in self.getRules():
            rulesByLhsName[r.leftHandSymbol.name].append(r)
        for name in rulesByLhsName:
            if len(rulesByLhsName[name]) > 1:
                for rule in rulesByLhsName[name]:
                    yield rule

    def getLhsNames(self):
        lhsNames = set()
        for r in self.getRules():
            lhsNames.add(r.leftHandSymbol.name)
        return lhsNames

    def getRhsNonterminals(self):
        for r in self.getRules():
            for t in r.rightHandSymbols:
                if not t.isTerminal:
                    yield r, t

    def getRulesThatHaveSep(self):
        for r in self.getRules():
            if r.separator:
                yield r

    def getNonrepeatingRules(self):
        for r in self.getRules():
            if not r.isRepeating:
                yield r


