from plcc.code.structures import Module
from plcc.code.structures import Class
from plcc.code.structures import StrClassName
from plcc.code.structures import ClassName
from plcc.code.structures import BaseClassName
from plcc.code.structures import VariableName
from plcc.code.structures import TypeName
from plcc.code.structures import ListVariableName
from plcc.code.structures import ListTypeName
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
                name=BaseClassName(symbol),
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
        return ClassName(rule.leftHandSymbol)

    def getStartClassName(self):
        return StrClassName('_Start')

    def getBaseClassName(self, rule):
        if not rule.leftHandSymbol.givenName:
            return None
        else:
            return BaseClassName(rule.leftHandSymbol)

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
        n = VariableName(symbol)
        t = TypeName(symbol)
        f = FieldDeclaration(name=n, type=t)
        return f

    def makeListField(self, symbol):
        n = ListVariableName(symbol)
        t = ListTypeName(symbol)
        f = FieldDeclaration(name=n, type=t)
        return f

    def makeConstructor(self, className, fields):
        parameters = self.makeConstructorParameters(fields)
        body = self.makeConstructorBody(fields)
        constructor=Constructor(className=className, parameters=parameters, assignments=body)
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
