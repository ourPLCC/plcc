class Presenter:
    def __init__(self, language):
        self._language = language

    def presentClass(self, class_):
        string = ''
        string += self.makeOpen(class_.name, class_.extends)
        string += self.makeFields(class_.fields)
        string += self.makeMethods(class_.methods)
        string += self.makeClose()
        return string

    def makeOpen(self, name, extends):
        return self._language.makeClassOpening(
            name=self.makeClassName(name),
            extends=self.makeClassName(extends)
        )

    def makeClassName(self, name):
        return self._language.toClassName(name.getClassName())
