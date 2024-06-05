from plcc.code.structures import Module
from plcc.code.structures import Class
from plcc.code.structures import ClassName
from plcc.code.structures import UnresolvedClassName


class AstClassGenerator:
    def generate(self, bnfspec):
        if not bnfspec or not list(bnfspec.getRules()):
            return []

        m = Module()
        rule = list(bnfspec.getRules())[0]

        c = Class(
            UnresolvedClassName(rule.leftHandSymbol),
            extends=ClassName('_Start')
        )

        m.classes.append(c)

        return [m]
