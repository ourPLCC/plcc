from .default import DefaultTranslator


class JavaTranslator(DefaultTranslator):
    def toListTypeName(self, name):
        return f'List<{name}>'

    def toFieldReference(self, name):
        return f'this.{name}'

    def toAssignmentStatement(self, lhs, rhs):
        return f'{lhs} = {rhs};'
