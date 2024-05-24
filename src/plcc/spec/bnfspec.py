from collections import defaultdict


class BnfSpec:
    def __init__(self, bnfRules):
        self._bnfRules = bnfRules

    def getTerminals(self):
        for rule in self._bnfRules:
            for tnt in rule.tnts:
                if tnt.isTerminal:
                    yield rule, tnt
            if rule.sep:
                yield rule, rule.sep

    def getRules(self):
        for rule in self._bnfRules:
            yield rule

    def getRulesWithDuplicateLhsNames(self):
        rulesByLhsName = defaultdict(list)
        for r in self.getRules():
            rulesByLhsName[r.lhs.name].append(r)
        for name in rulesByLhsName:
            if len(rulesByLhsName[name]) > 1:
                for rule in rulesByLhsName[name]:
                    yield rule

    def getLhsNames(self):
        lhsNames = set()
        for r in self.getRules():
            lhsNames.add(r.lhs.name)
        return lhsNames

    def getRhsNonterminals(self):
        for r in self.getRules():
            for t in r.tnts:
                if not t.isTerminal:
                    yield r, t

    def getRulesThatHaveSep(self):
        for r in self.getRules():
            if r.sep:
                yield r

    def getNonrepeatingRules(self):
        for r in self.getRules():
            if not r.isRepeating:
                yield r
