from collections import defaultdict


from .bnfrule import TntType


class BnfSpec:
    def __init__(self, bnfRules):
        self._bnfRules = bnfRules

    def getTerminals(self):
        for rule in self._bnfRules:
            for tnt in rule.tnts:
                if tnt.type == TntType.TERMINAL:
                    yield rule, tnt
            if rule.sep:
                yield rule, rule.sep

    def getNonterminals(self):
        for rule in self._bnfRules:
            print(rule)
            yield rule, rule.lhs
            for tnt in rule.tnts:
                if tnt.type == TntType.NONTERMINAL:
                    yield rule, tnt

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
