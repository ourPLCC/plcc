from plcc.code.structures import Module
from plcc.code.structures import Class
from plcc.code.structures import ClassName
from plcc.code.structures import UnresolvedClassName
from plcc.code.structures import UnresolvedVariableName
from plcc.code.structures import UnresolvedTypeName
from plcc.code.structures import UnresolvedListVariableName
from plcc.code.structures import UnresolvedListTypeName
from plcc.code.structures import FieldDeclaration
from plcc.code.structures import Parameter
from plcc.code.structures import FieldInitialization
from plcc.code.structures import FieldReference
from plcc.code.structures import Constructor


class AstClassGenerator:

    def generate(self, bnfspec):
        if not bnfspec or not list(bnfspec.getRules()):
            return []
        m = Module()
        rule = list(bnfspec.getRules())[0]
        c = self.makeClass(rule)
        m.classes.append(c)
        return [m]

    def makeClass(self, rule):
        className = self.getClassNameForRule(rule)
        extends = self.getStartClassName()
        fields = self.makeFields(rule)
        constructor = self.makeConstructor(className, fields)
        class_ = Class(
            name=className,
            extends=extends,
            fields=fields,
            constructor=constructor
        )
        return class_

    def getClassNameForRule(self, rule):
        return UnresolvedClassName(rule.leftHandSymbol)

    def getStartClassName(self):
        return ClassName('_Start')

    def makeFields(self, rule):
        fields = []
        for s in rule.rightHandSymbols:
            if s.isCapture:
                if not rule.isRepeating:
                    f = self.makeField(s)
                else:
                    f = self.makeListField(s)
                fields.append(f)
        return fields

    def makeField(self, symbol):
        n = UnresolvedVariableName(symbol)
        t = UnresolvedTypeName(symbol)
        f = FieldDeclaration(name=n, type=t)
        return f

    def makeListField(self, symbol):
        n = UnresolvedListVariableName(symbol)
        t = UnresolvedListTypeName(symbol)
        f = FieldDeclaration(name=n, type=t)
        return f

    def makeConstructor(self, className, fields):
        parameters = self.makeConstructorParameters(fields)
        body = self.makeConstructorBody(fields)
        constructor=Constructor(className=className, parameters=parameters, body=body)
        return constructor

    def makeConstructorParameters(self, fields):
        params = []
        for f in fields:
            p = Parameter(name=f.name, type=f.type)
            params.append(p)
        return params

    def makeConstructorBody(self, fields):
        inits = []
        for f in fields:
            init = FieldInitialization(
                field=FieldReference(name=f.name),
                parameter=f.name
            )
            inits.append(init)

        return inits

