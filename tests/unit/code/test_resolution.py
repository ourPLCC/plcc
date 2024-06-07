import pytest


from plcc.spec.symbol import Symbol

from plcc.code.render.default import Default
from plcc.code.render.java import Java
from plcc.code.render.python import Python
from plcc.code.structures import BaseClassName
from plcc.code.structures import ClassName
from plcc.code.structures import TypeName
from plcc.code.structures import VariableName
from plcc.code.structures import ListVariableName
from plcc.code.structures import ListTypeName
from plcc.code.structures import FieldReference
from plcc.code.structures import AssignVariableToField
from plcc.code.structures import Parameter
from plcc.code.structures import Constructor
from plcc.code.structures import FieldDeclaration


def test_TypeName_resolves_to_capitalized_symbol_name():
    unrendered = givenTypeName(name='cat', givenName='pet')
    rendered = whenRenderedByDefault(unrendered)
    assert rendered == 'Cat'


def test_VariableName_resolves_to_symbol_given_name():
    unrendered = givenVariableName(name='cat', givenName='pet')
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'pet'


def test_VariableName_if_no_given_name_resolves_to_symbol_name():
    unrendered = givenVariableName(name='cat', givenName=None)
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'cat'


def test_TypeName_if_terminal_resolves_to_Token():
    unrendered = givenTypeName(name='cat', givenName='pet', isTerminal=True)
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'Token'


def test_ClassName_resolves_to_symbol_given_name():
    unrendered = givenClassName(name='cat', givenName='pet')
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'pet'


def test_ClassName_resolves_to_capitalized_symbol_name_if_no_given_name():
    unrendered = givenClassName(name='cat', givenName=None)
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'Cat'


def test_BaseClassName_resolves_to_capitalized_symbol_name():
    unrendered = givenBaseClassName(name='cat', givenName='Pet')
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'Cat'


def test_ListVariableName_resolves_to_given_name():
    unrendered = givenListVariableName(name='cat', givenName='fluffy')
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'fluffy'


def test_ListVariableName_if_no_given_name_resolves_to_symbol_name_appended_with_List():
    unrendered = givenListVariableName(name='cat', givenName='')
    rendered = whenRendered(unrendered, using=Default())
    assert rendered == 'catList'


def test_in_Java_ListTypeName_resolves_to_List_parameterized_by_its_rendered_type_name():
    unrendered = givenListTypeName(name='cat', givenName='fluffy')
    rendered = whenRendered(unrendered, using=Java())
    assert rendered == 'List<Cat>'


def test_in_Python_ListTypeName_resolves_to_square_brackets_containing_its_rendered_type_name():
    unrendered = givenListTypeName(name='cat', givenName='fluffy')
    rendered = whenRendered(unrendered, using=Python())
    assert rendered == '[Cat]'


def test_in_Java_FieldReference_resolves_to_this_dot_variable_name():
    unrendered = givenFieldReference('cat')
    rendered = whenRenderedByJava(unrendered)
    assert rendered == 'this.cat'


def test_in_Python_FieldReference_resolves_to_self_dot_variable_name():
    unrendered = givenFieldReference('cat')
    rendered = whenRenderedByPython(unrendered)
    assert rendered == 'self.cat'


def test_in_Java_FieldInitialization():
    unrendered = givenAssignVariableToField('cat')
    rendered = whenRenderedByJava(unrendered)
    assert rendered == 'this.cat = cat;'


def test_in_Python_FieldInitialization():
    unrendered = givenAssignVariableToField('cat')
    rendered = whenRenderedByPython(unrendered)
    assert rendered == 'self.cat = cat'


def test_in_Java_Parameter():
    param = givenParameter('cat')
    rendered = whenRenderedByJava(param)
    assert rendered == 'Cat cat'


def test_in_Python_Parameter():
    param = givenParameter('cat')
    rendered = whenRenderedByPython(param)
    assert rendered == 'cat: Cat'


def test_in_Java_list_Parameter():
    param = givenListParameter('cat')
    rendered = whenRenderedByJava(param)
    assert rendered == 'List<Cat> catList'


def test_in_Python_list_Parameter():
    param = givenListParameter('cat')
    rendered = whenRenderedByPython(param)
    assert rendered == 'catList: [Cat]'


def test_in_Java_constructor():
    constructor = givenSimpleConstructor('cat', ['fur', 'tail', 'claws'])
    rendered = whenRenderedByJava(constructor)
    assert rendered == [
        'public Cat(Fur fur, Tail tail, Claws claws) {',
        '    this.fur = fur;',
        '    this.tail = tail;',
        '    this.claws = claws;',
        '}'
    ]


def test_in_Python_constructor():
    constructor = givenSimpleConstructor('cat', ['fur', 'tail', 'claws'])
    rendered = whenRenderedByPython(constructor)
    assert rendered == [
        'def __init__(self, fur: Fur, tail: Tail, claws: Claws):',
        '    self.fur = fur',
        '    self.tail = tail',
        '    self.claws = claws'
    ]


def test_in_Java_FieldDeclaration():
    decl = givenFieldDeclaration('cat')
    rendered = whenRenderedByJava(decl)
    assert rendered == 'public Cat cat;'


def test_in_Python_FieldDeclaration_is_done_in_constructor_so_empty():
    decl = givenFieldDeclaration('cat')
    rendered = whenRenderedByPython(decl)
    assert rendered == ''


def givenFieldDeclaration(name):
    return FieldDeclaration(
        givenVariableName(name=name),
        givenTypeName(name=name)
    )


def givenFieldReference(name):
    return FieldReference(given(VariableName, name))


def givenParameter(name):
    symbol = makeSymbol(name)
    name = VariableName(symbol)
    type = TypeName(symbol)
    param = Parameter(name, type)
    return param


def givenListParameter(name):
    symbol = makeSymbol(name)
    name = ListVariableName(symbol)
    type = ListTypeName(symbol)
    param = Parameter(name, type)
    return param


def givenSimpleConstructor(name, fields):
    className = givenClassName(name=name)
    params = []
    for f in fields:
        p = givenParameter(f)
        params.append(p)
    assignments = []
    for f in fields:
        a = givenAssignVariableToField(f)
        assignments.append(a)
    return Constructor(className, params, assignments)


def givenAssignVariableToField(name):
    fieldRef = givenFieldReference(name)
    param = given(VariableName, name)
    return AssignVariableToField(fieldRef, param)


def givenTypeName(name='', givenName='', isTerminal=False):
    return given(type=TypeName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenVariableName(name='', givenName='', isTerminal=False):
    return given(type=VariableName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenClassName(name='', givenName='', isTerminal=False):
    return given(type=ClassName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenBaseClassName(name='', givenName='', isTerminal=False):
    return given(type=BaseClassName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenListVariableName(name='', givenName='', isTerminal=False):
    return given(type=ListVariableName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenListTypeName(name='', givenName='', isTerminal=False):
    return given(type=ListTypeName, name=name, givenName=givenName, isTerminal=isTerminal)


def given(type, name, givenName='', isTerminal=False):
    symbol = makeSymbol(name=name, given=givenName, isTerminal=isTerminal)
    unrenderedName = type(symbol)
    return unrenderedName


def makeSymbol(name=None, given=None, isTerminal=None):
    return Symbol(
        name=name,
        givenName=given,
        isCapture=None,
        isTerminal=isTerminal
    )


def whenRenderedByDefault(unrendered):
    return whenRendered(unrendered, Default())


def whenRenderedByPython(unrendered):
    return whenRendered(unrendered, Python())


def whenRenderedByJava(unrendered):
    return whenRendered(unrendered, Java())


def whenRendered(unrendered, using):
    return unrendered.renderWith(using)
