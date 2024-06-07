from .default import Default


class Java(Default):
    def renderListTypeName(self, name):
        return f'List<{name}>'

    def renderFieldReference(self, name):
        return f'this.{name}'

    def renderAssignmentStatement(self, lhs, rhs):
        return f'{lhs} = {rhs};'

    def renderParameter(self, name, type):
        return f'{type} {name}'

    def renderConstructor(self, className, params, assignments):
        pstr = ', '.join(params)
        open = [ f'public {className}({pstr}) {{' ]
        body = self.indentLines(assignments, 1)
        close = [ '}' ]
        return open + body + close

    def renderFieldDeclaration(self, name, type):
        return f'public {type} {name};'
