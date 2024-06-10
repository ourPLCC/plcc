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

    def renderClass(self, name, extends, fields, methods):
        open = self.makeClassOpen(extends, name)
        body = self.makeClassBody(fields, methods)
        return open + body

    def makeClassOpen(self, extends, name):
        ext = '' if extends is None else f'({extends})'
        open = [f'class {name}{ext}:']
        return open

    def makeClassBody(self, fields, methods):
        blankLine=''
        body = []
        fields = list(filter(lambda f: bool(f), fields))
        body.extend(fields)
        for m in methods:
            body.extend(m)
            body.append(blankLine)
        body = self.indentLines(body, levels=1)
        return body

