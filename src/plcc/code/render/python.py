from .default import Default


class Python(Default):
    def renderListTypeName(self, name):
        return f'[{name}]'

    def renderFieldReference(self, name):
        return f'self.{name}'

    def renderAssignmentStatement(self, lhs, rhs):
        return f'{lhs} = {rhs}'

    def renderParameter(self, name, type):
        return f'{name}: {type}'

    def renderConstructor(self, className, params, assignments):
        pstr = ', '.join(['self'] + params)
        open = [ f'def __init__({pstr}):' ]
        body = self.indentLines(assignments, 1)
        return open + body

    def renderFieldDeclaration(self, name, type):
        return ''

