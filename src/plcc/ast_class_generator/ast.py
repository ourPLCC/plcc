from plcc.code.structures import Module
from plcc.code.structures import Class
from plcc.code.structures import ClassName
from plcc.code.structures import UnresolvedClassName
from plcc.code.structures import UnresolvedVariableName
from plcc.code.structures import UnresolvedTypeName
from plcc.code.structures import FieldDeclaration


class AstClassGenerator:
    def generate(self, bnfspec):
        if not bnfspec or not list(bnfspec.getRules()):
            return []

        m = Module()
        rule = list(bnfspec.getRules())[0]

        fields = []
        for s in rule.rightHandSymbols:
            n = UnresolvedVariableName(s)
            t = UnresolvedTypeName(s)
            f = FieldDeclaration(name=n, type=t)
            fields.append(f)

        c = Class(
            UnresolvedClassName(rule.leftHandSymbol),
            extends=ClassName('_Start'),
            fields=fields
        )

        m.classes.append(c)

        return [m]
