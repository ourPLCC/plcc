from .stubs import Stubs


class PythonStubs(Stubs):
    def __init__(self, stubs=None):
        super().__init__(stubs)

    def getLineComment(self):
        return '#'

    def getBlockCommentStart(self):
        return "'''"

    def getBlockCommentEnd(self):
        return "'''"

    def makeFieldDeclaration(self, type, name):
        return f'name = None'

    def makeFieldInitializer(self, name):
        return f'self.{name} = {name}'

    def makeParameterDeclaration(self, type, name):
        return f'{name}'

    def makeExtendsClause(self, type):
        return f'{type}'

    def makeCase(self, value):
        return f'case {value}:'

    def makeParseCaseReturn(self, cls):
        return f'return {cls}.parse(scn,trace)'

    def makeStub(self, cls, lhs, ext, ruleString, decls, params, inits, parse):
        return f"""\
#{cls}:top#
#{cls}:import#

# {ruleString}
class {cls}({ext}): #{cls}:class#

    className = "{cls}"
    ruleString = "{ruleString}"
{decls}

    def __init__({params}):
        #{cls}:init#
{inits}

#{cls}#
"""

    def makeAbstractStub(self, base, ext, cases):
        return f"""\
#{base}:top#
#{base}:import#

class {base}({ext}): #{base}:class#

    className = "{base}"

    #{base}#
"""
