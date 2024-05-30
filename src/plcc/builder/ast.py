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
        ...

    def makeStartClass(self):
        ...

    def makeAbstractBaseClasses(self, bnfSpec):
        ...

    def makeConcreteClasses(self, bnfSpec):
        ...

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
        return Name(
            name = bnfRule.leftHandSymbol.alt,
            isList = False,
            isFinal = True
        )

    def makeDefaultClassName(self, bnfRule):
        return Name(
            name = bnfRule.name,
            isList = False,
            isFinal = False
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
        return Name(
            name = symbol.alt if symbol.alt else symbol.name,
            isList = isRepeating,
            isFinal = bool(symbol.alt)
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

