from plcc.code.structures import Module
from plcc.code.structures import Class
from plcc.code.structures import ClassName
from plcc.code.structures import UnresolvedClassName
from plcc.code.structures import UnresolvedBaseClassName
from plcc.code.structures import UnresolvedVariableName
from plcc.code.structures import UnresolvedTypeName
from plcc.code.structures import UnresolvedListVariableName
from plcc.code.structures import UnresolvedListTypeName
from plcc.code.structures import FieldDeclaration
from plcc.code.structures import Parameter
from plcc.code.structures import AssignVariableToField
from plcc.code.structures import FieldReference
from plcc.code.structures import Constructor


class AstClassGenerator:
    def generate(self, bnfspec):
        if not bnfspec or not list(bnfspec.getRules()):
            return []
        firstRule = next(bnfspec.getRules())
        symsWithAlts = self.getSymbolsWithAlternativeDefinitions(bnfspec)
        modules = self.makeBaseClasses(bnfspec, symsWithAlts)
        modules.extend(self.makeClasses(bnfspec, firstRule, symsWithAlts))
        return modules

    def getSymbolsWithAlternativeDefinitions(self, bnfspec):
        symbolsWithAlternativeDefinitions = {}
        for r in bnfspec.getRulesWithDuplicateLhsNames():
            if r.leftHandSymbol.name not in symbolsWithAlternativeDefinitions:
                symbolsWithAlternativeDefinitions[r.leftHandSymbol.name] = r.leftHandSymbol
        return symbolsWithAlternativeDefinitions

    def makeBaseClasses(self, bnfspec, symsWithAlts):
        modules = []
        for symbol in symsWithAlts.values():
            c = Class(
                name=UnresolvedBaseClassName(symbol),
                constructor=None,
                extends=None,
                fields=[]
            )
            m = Module(classes=[c])
            modules.append(m)
        return modules

    def makeClasses(self, bnfspec, firstRule, symsWithAlts):
        modules = []
        for rule in bnfspec.getRules():
            m = Module()
            c = self.makeClass(rule, rule == firstRule, symsWithAlts)
            m.classes.append(c)
            modules.append(m)
        return modules

    def makeClass(self, rule, isFirstRule, alternatives):
        className = self.getClassNameForRule(rule)
        extends = self.getStartClassName() if isFirstRule else self.getBaseClassName(rule)
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

    def getBaseClassName(self, rule):
        if not rule.leftHandSymbol.givenName:
            return None
        else:
            return UnresolvedBaseClassName(rule.leftHandSymbol)

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
            init = AssignVariableToField(
                lhs=FieldReference(name=f.name),
                rhs=f.name
            )
            inits.append(init)

        return inits
