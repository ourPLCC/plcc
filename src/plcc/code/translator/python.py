from .default import DefaultTranslator


class PythonTranslator(DefaultTranslator):
    def toListTypeName(self, name):
        return f'[{name}]'

    def toFieldReference(self, name):
        return f'self.{name}'
