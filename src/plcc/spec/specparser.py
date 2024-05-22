from .lexparser import LexParser
from .bnfparser import BnfParser
from .semparser import SemParser
from .spec import Spec


class SpecParser():
    def parse(self, sections):
        lexRules = LexParser().parse(sections[0])
        bnfRules = BnfParser().parse(sections[1])
        semRules = []
        for s in sections[2:]:
            semRules.append(SemParser().parse(s))
        return Spec(lexRules, bnfRules, semRules)
