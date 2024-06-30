from dataclasses import is_dataclass, fields

from plcc.visitor_pattern import Transformer


class BottomUp:
    def __init__(self, visitor):
        self.visitor = visitor

    def visit(self, obj):
        '''
        Apply visitor to each dataclass object, bottom up.
        Results from visiting a dataclass object's children are passed to the
        visit method as keyword arguments. For example if the dataclass object
        has fields x and y, then those fields are visited first and their
        results are passed to the visit call for the original object as
        keyword arguments x and y (roughly v.visit(o, x=v.visit(o.x), y=v.visit(o.y))).
        '''
        if is_dataclass(obj):
            d = {field.name: getattr(obj, field.name) for field in fields(obj)}
            visitedFields = {k: self.visit(d[k]) for k in d}
            return self.visitor.visit(obj, **visitedFields)
        elif isinstance(obj, list):
            return [self.visit(e) for e in obj]
        else:
            return obj


class Indenter:
    '''
    Does not add indent to the start of an empty line.
    '''
    def __init__(self, indent='    ', newline='\n'):
        self.NEWLINE=newline
        self.INDENT=indent

    def indent(self, stringOrList):
        if isinstance(stringOrList, str):
            return self.indentString(stringOrList)
        else:
            return self.indentList(stringOrList)

    def indentString(self, string):
        s = string.split(self.NEWLINE)
        return self.NEWLINE.join(self.indentList(s))

    def indentList(self, list_):
        lines = []
        for line in list_:
            if line:
                indentedLine = f'{self.INDENT}{line}'
            else:
                indentedLine = line
            lines.append(indentedLine)
        return lines


class CodePresenter(Transformer):
    def __init__(self, indenter=None):
        self.indenter = indenter if indenter else Indenter()

    def present(self, code):
        return BottomUp(self).visit(code)

    def indent_and_join(self, block):
        if isinstance(block, str):
            return self.indenter.indent(block)
        else:
            return '\n'.join(self.indenter.indent(block))

    def visit_TypeName(self, obj, symbol):
        return symbol.getTypeName()

    def visit_VariableName(self, obj, symbol):
        return symbol.getVariableName()

    def visit_ListVariableName(self, obj, symbol):
        return symbol.getListVariableName()

    def visit_ClassName(self, obj, symbol):
        return symbol.getClassName()

    def visit_BaseClassName(self, obj, symbol):
        return symbol.getBaseClassName()

    def visit_Symbol(self, obj, **kws):
        return obj

    def visit_StrClassName(self, obj, name):
        return name


class JavaPresenter(CodePresenter):

    def visit_Class(self, obj, name, extends, fields, constructor):
        extends = f' extends {extends}' if extends else ''
        fields = self.indent_and_join(fields)
        constructor = self.indent_and_join(constructor)

        newline = '\n'
        open_ = f'public class {name}{extends} {{'
        close_ = '}'
        result = open_ + newline + fields + newline + newline + constructor + close_ + newline
        return result

    def visit_FieldDeclaration(self, obj, name, type):
        return f'public {type} {name};'

    def visit_Constructor(self, obj, className, parameters, assignments):
        parameters = ', '.join(parameters)
        open_ =  f'public {className}({parameters}) {{'
        newline = '\n'
        assignments = self.indent_and_join(assignments)
        close_ = '}'
        result = open_ + newline + assignments + newline + close_ + newline
        return result

    def visit_Parameter(self, obj, name, type):
        return f'{type} {name}'

    def visit_AssignVariableToField(self, obj, lhs, rhs):
        return f'{lhs} = {rhs};'

    def visit_FieldReference(self, obj, name):
        return f'this.{name}'

    def visit_ListTypeName(self, obj, symbol):
        return f'List<{symbol.getTypeName()}>'


class PythonPresenter(CodePresenter):

    def visit_Class(self, obj, name, extends, fields, constructor):
        extends = f'({extends})' if extends else ''
        constructor = self.indent_and_join(constructor)
        return f'''\
class {name}{extends}:
{constructor}'''

    def visit_FieldDeclaration(self, obj, name, type):
        return ''

    def visit_Constructor(self, obj, className, parameters, assignments):
        parameters = ', '.join(parameters)
        assignments = self.indent_and_join(assignments)
        return f'''\
def __init__(self, {parameters}):
{assignments}
'''

    def visit_Parameter(self, obj, name, type):
        return f'{name}: {type}'

    def visit_AssignVariableToField(self, obj, lhs, rhs):
        return f'{lhs} = {rhs}'

    def visit_FieldReference(self, obj, name):
        return f'self.{name}'

    def visit_ListTypeName(self, obj, symbol):
        return f'[{symbol.getTypeName()}]'

