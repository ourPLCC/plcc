class Default:
    def renderTypeName(self, name):
        return name.capitalize()

    def renderVariableName(self, name):
        return name

    def renderClassName(self, name):
        return name.capitalize()

    def renderBaseClassName(self, name):
        return name.capitalize()

    def renderListVariableName(self, name):
        return f'{name}List'

    def indentLines(self, lines, levels, indent='    '):
        indent = indent * levels
        return [ indent+line for line in lines ]
