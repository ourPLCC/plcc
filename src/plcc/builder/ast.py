from .struct import *


class AstClassHierarchyMaker:

    def make(self, spec):
        classes = []
        classes.append(self.makeTokenClass(spec.lexSpec))
        classes.append(self.makeStartClass())
        classes.extend(self.makeAbstractBaseClasses(spec.bnfSpec))
        classes.extend(self.makeConcreteClasses(spec.bnfSpec))
        return classes

    def makeTokenClass(self, lexSpec):
        return Enum(
            name=self.makeTokenClassName(),
            values=self.makeTokenNames(lexSpec)
        )

    def makeTokenClassName(self):
        return ClassName(
            name = 'Token'
        )

    def makeTokenNames(self, lexSpec):
        names = []
        for nameString in lexSpec.getTokenNames():
            names.append(self.makeTokenName(nameString))
        return names

    def makeTokenName(self, string):
        return ConstantName(string)

    def makeStartClass(self):
        return Class(
            name=ClassName('_Start'),
            extends=None,
            fields=[],
            methods=[
                self.makeStartRunMethod()
            ]
        )

    def makeStartRunMethod(self):
        return Method(
            name=MethodName('_run'),
            returnType=Type('void'),
            parameters=[],
            body=[
                PrintSelfAsStringStatement()
            ]
        )

    def makeAbstractBaseClasses(self, bnfSpec):
        classes = []
        for symbol in bnfSpec.getAbstractBaseSymbols():
            classes.append(self.makeAbstractBaseClass(symbol))
        return classes

    def makeAbstractBaseClass(self, symbol):
        return Class(
            name=self.makeAbstractBaseClassName(symbol),
            extends=None,
            fields=[],
            methods=[]
        )

    def makeAbstractBaseClassName(self, symbol):
        return self.makeDefaultClassName(symbol)

    def makeConcreteClasses(self, bnfSpec):
        classes = []
        for rule in bnfSpec.getRules():
            classes.append(self.makeClass(rule))
        return classes

    def makeClass(self, bnfRule):
        return Class(
            name=self.makeClassName(bnfRule),
            extends=self.makeExtends(bnfRule),
            fields=self.makeFields(bnfRule),
            methods=self.makeMethods(bnfRule)
        )

    def makeClassName(self, bnfRule):
        if bnfRule.leftHandSymbol.alt:
            return self.makeAltClassName(bnfRule)
        else:
            return self.makeDefaultClassName(bnfRule)

    def makeAltClassName(self, bnfRule):
        return ClassName(
            name = bnfRule.leftHandSymbol.alt
        )

    def makeDefaultClassName(self, bnfRule):
        return ClassName(
            name = bnfRule.leftHandSymbol.name
        )

    def makeExtends(self, bnfRule):
        if bnfRule.isAlternativeRule:
            return self.makeDefaultClassName(bnfRule)
        elif bnfRule.isFirstRule:
            return self.makeStartClassName()
        else:
            return None

    def makeFields(self, bnfRule):
        fields = []
        for s in bnfRule.rightHandSymbols:
            fields.append(self.makeField(s))

    def makeField(self, symbol, isRepeating):
        return Variable(
            name=self.makeFieldName(symbol, isRepeating),
            type=self.makeFieldType(symbol, isRepeating),
            isField=True
        )

    def makeFieldName(self, symbol, isRepeating):
        return VariableName(
            name = symbol.alt if symbol.alt else symbol.name,
            isList = isRepeating
        )

    def makeFieldType(self, symbol, isRepeating):
        return Type(
            name = symbol.name,
            isList = isRepeating
        )

    def makeMethods(self, bnfRule):
        return [
            self.makeConstructor(bnfRule)
        ]

    def makeConstructor(self, bnfRule):
        return Method(
            name = self.makeClassName(bnfRule),
            parameters = self.makeFields(bnfRule),
            returnType = None,
            body = self.makeConstructorBody(bnfRule)
        )

    def makeConstructorBody(self, bnfRule):
        body = []
        for f in self.makeFields(bnfRule):
            body.append(self.makeConstructorAssignmentStatement(f))
        return body

    def makeConstructorAssignmentStatement(self, field):
        return ConstructorAssignmentStatement(
            lhs=field,
            rhs=field.toNonField()
        )

