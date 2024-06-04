from ..class_ import Class
from ..module import Module
from ..names import UnresolvedClassName
from ..names import ClassName


class AstGenerator:
    def generate(self, bnfspec):
        if not bnfspec or not list(bnfspec.getRules()):
            return []

        m = Module()
        rule = list(bnfspec.getRules())[0]
        c = Class(UnresolvedClassName(rule.leftHandSymbol), extends=ClassName('_Start'))
        m.classes.append(c)

        return [m]
