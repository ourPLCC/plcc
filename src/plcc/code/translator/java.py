from .default import DefaultTranslator


class JavaTranslator(DefaultTranslator):
    def toListTypeName(self, name):
        return f'List<{name}>'

    def toFieldReference(self, name):
        return f'this.{name}'

    def toAssignmentStatement(self, lhs, rhs):
        return f'{lhs} = {rhs};'

    def toParameter(self, name, type):
        return f'{type} {name}'

    def toConstructor(self, className, params, assignments):
        pstr = ', '.join(params)
        open = [ f'public {className}({pstr}) {{' ]
        body = self.indentLines(assignments, 1)
        close = [ '}' ]
        return open + body + close

    def toFieldDeclaration(self, name, type):
        return f'public {type} {name};'
