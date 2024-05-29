class TreeNodeMaker:
    def makeFile(self, bnfRule):
        bnfRule.line

        baseName = Name(
            name = bnfRule.name,
            isList = False,
            isFinal = False
        )

        if bnfRule.leftHandSymbol.alt:
            className = Name(
                name = bnfRule.leftHandSymbol.alt,
                isList = False,
                isFinal = True
            )
        else:
            className = baseName

        if bnfRule.isAlternativeRule:
            extends = baseName
        elif bnfRule.isFirstRule:
            extends = START_TYPE
        else:
            extends = None

        fields = []
        for s in bnfRule.rightHandSymbols:
            fieldName = Name(
                name = s.alt if s.alt else s.name,
                isList = rule.isRepeating,
                isFinal = bool(s.alt)
            )

            fieldType = Type(
                name = s.name,
                isList = True,
                isFinal = bnfRule.isRepeating
            )

            field = Variable(fieldName, fieldType)
            fields.append(field)

        Method(
            name = className,
            parameters = fields,
            returnType = None,
            body = None
        )


        constructorBody = '\n'.join(self.language.indentLines(levels=2, lines=[
            self.language.getConstructorFieldInit(fieldName) for f in fields
        ]))

        constructor = Method(
            name = className,
            body = constructorBody,
            returnType = None,
            comment = None
        )

        class_ = Class(
            name = className,
            extends = extends,
            fields = fields,
            methods = [constructor],
            comment = None
        )

        return File(
            name = fileName,
            imports = self.language.getTreeNodeImports(),
            class_ = class_
        )
