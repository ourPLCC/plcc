from .lexrule import LexRule
from .bnfrule import BnfRule
from .semrule import SemRule


class Spec:
    def __init__(self):
        self._bnfRules = None
        self._lexRules = None
        self._semRuleSections = []

    def setLexRules(self, lexRules):
        self._lexRules = lexRules

    def setBnfRules(self, bnfRules):
        self._bnfRules = bnfRules

    def addSemRuleSection(self, semRules):
        self._semRuleSections.append(semRule)
