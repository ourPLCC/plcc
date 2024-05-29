class TreeNodeMaker:
    def makeFile(self, bnfRule):
        bnfRule.line

        if bnfRule.leftHandSymbol.alt:
            className = bnfRule.leftHandSymbol.alt
        else:
            className = self.language.getClassName(bnfRule.name)

        if bnfRule.isAlternativeRule:
            extends = self.language.getClassName(bnfRule.name)
        elif bnfRule.isFirstRule:
            extends = self.language.getStartClassName()
        else:
            extends = None

        fields = []
        for s in bnfRule.rightHandSymbols:
            if s.alt:
                fieldName = self.language.alt
            else:
                if bnfRule.isRepeating:
                    fieldName = self.language.getListFieldName(s.name)
                else:
                    fieldName = self.language.getFieldName(s.name)

            if bnfRule.isRepeating:
                fieldType = self.language.getListFieldType(s.name)
            else:
                fieldType = self.language.getFieldType(s.name)

            field = Variable(fieldName, fieldType)
            fields.append(field)

        fileName = self.language.getFileNameForClass(className)

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
