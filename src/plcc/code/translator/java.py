class JavaTranslator:
    def toTypeName(self, name):
        return name.capitalize()

    def toVariableName(self, name):
        return name

    def toClassName(self, name):
        return name.capitalize()

    def toBaseClassName(self, name):
        return name.capitalize()
