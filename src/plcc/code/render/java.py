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

    def renderClass(self, name, extends, fields, methods):
        open = self.makeClassOpen(extends, name)
        close = self.makeClassClose()
        body = self.makeClassBody(fields, methods)
        return open + body + close

    def makeClassOpen(self, extends, name):
        ext = '' if extends is None else f' extends {extends}'
        open = [f'public class {name}{ext} {{']
        return open

    def makeClassBody(self, fields, methods):
        blankLine=''
        body = []
        body.extend(fields)
        body.append(blankLine)
        for m in methods:
            body.extend(m)
            body.append(blankLine)
        body = self.indentLines(body, levels=1)
        return body

    def makeClassClose(self):
        return [f'}}']

