import pytest


from plcc.spec.symbol import Symbol

from plcc.code.translator.default import DefaultTranslator
from plcc.code.translator.java import JavaTranslator
from plcc.code.translator.python import PythonTranslator
from plcc.code.structures import UnresolvedBaseClassName
from plcc.code.structures import UnresolvedClassName
from plcc.code.structures import UnresolvedTypeName
from plcc.code.structures import UnresolvedVariableName
from plcc.code.structures import UnresolvedListVariableName
from plcc.code.structures import UnresolvedListTypeName
from plcc.code.structures import FieldReference
from plcc.code.structures import AssignVariableToField
from plcc.code.structures import Parameter
from plcc.code.structures import Constructor
from plcc.code.structures import FieldDeclaration


def test_UnresolvedTypeName_resolves_to_capitalized_symbol_name():
    unresolved = givenUnresolvedTypeName(name='cat', givenName='pet')
    resolved = whenResolvedByDefault(unresolved)
    assert resolved == 'Cat'

def test_UnresolvedVariableName_resolves_to_symbol_given_name():
    unresolved = givenUnresolvedVariableName(name='cat', givenName='pet')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'pet'


def test_UnresolvedVariableName_if_no_given_name_resolves_to_symbol_name():
    unresolved = givenUnresolvedVariableName(name='cat', givenName=None)
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'cat'


def test_UnresolvedTypeName_if_terminal_resolves_to_Token():
    unresolved = givenUnresolvedTypeName(name='cat', givenName='pet', isTerminal=True)
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'Token'


def test_UnresolvedClassName_resolves_to_symbol_given_name():
    unresolved = givenUnresolvedClassName(name='cat', givenName='pet')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'pet'


def test_UnresolvedClassName_resolves_to_capitalized_symbol_name_if_no_given_name():
    unresolved = givenUnresolvedClassName(name='cat', givenName=None)
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'Cat'


def test_UnresolvedBaseClassName_resolves_to_capitalized_symbol_name():
    unresolved = givenUnresolvedBaseClassName(name='cat', givenName='Pet')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'Cat'


def test_UnresolvedListVariableName_resolves_to_given_name():
    unresolved = givenUnresolvedListVariableName(name='cat', givenName='fluffy')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'fluffy'


def test_UnresolvedListVariableName_if_no_given_name_resolves_to_symbol_name_appended_with_List():
    unresolved = givenUnresolvedListVariableName(name='cat', givenName='')
    resolved = whenResolve(unresolved, using=DefaultTranslator())
    assert resolved == 'catList'


def test_in_Java_UnresolvedListTypeName_resolves_to_List_parameterized_by_its_resolved_type_name():
    unresolved = givenUnresolvedListTypeName(name='cat', givenName='fluffy')
    resolved = whenResolve(unresolved, using=JavaTranslator())
    assert resolved == 'List<Cat>'


def test_in_Python_UnresolvedListTypeName_resolves_to_square_brackets_containing_its_resolved_type_name():
    unresolved = givenUnresolvedListTypeName(name='cat', givenName='fluffy')
    resolved = whenResolve(unresolved, using=PythonTranslator())
    assert resolved == '[Cat]'


def test_in_Java_FieldReference_resolves_to_this_dot_variable_name():
    unresolved = givenFieldReference('cat')
    resolved = whenResolvedByJava(unresolved)
    assert resolved == 'this.cat'


def test_in_Python_FieldReference_resolves_to_self_dot_variable_name():
    unresolved = givenFieldReference('cat')
    resolved = whenResolvedByPython(unresolved)
    assert resolved == 'self.cat'


def test_in_Java_FieldInitialization():
    unresolved = givenAssignVariableToField('cat')
    resolved = whenResolvedByJava(unresolved)
    assert resolved == 'this.cat = cat;'


def test_in_Python_FieldInitialization():
    unresolved = givenAssignVariableToField('cat')
    resolved = whenResolvedByPython(unresolved)
    assert resolved == 'self.cat = cat'


def test_in_Java_Parameter():
    param = givenParameter('cat')
    resolved = whenResolvedByJava(param)
    assert resolved == 'Cat cat'


def test_in_Python_Parameter():
    param = givenParameter('cat')
    resolved = whenResolvedByPython(param)
    assert resolved == 'cat: Cat'


def test_in_Java_list_Parameter():
    param = givenListParameter('cat')
    resolved = whenResolvedByJava(param)
    assert resolved == 'List<Cat> catList'


def test_in_Python_list_Parameter():
    param = givenListParameter('cat')
    resolved = whenResolvedByPython(param)
    assert resolved == 'catList: [Cat]'


def test_in_Java_constructor():
    constructor = givenSimpleConstructor('cat', ['fur', 'tail', 'claws'])
    resolved = whenResolvedByJava(constructor)
    assert resolved == [
        'public Cat(Fur fur, Tail tail, Claws claws) {',
        '    this.fur = fur;',
        '    this.tail = tail;',
        '    this.claws = claws;',
        '}'
    ]


def test_in_Python_constructor():
    constructor = givenSimpleConstructor('cat', ['fur', 'tail', 'claws'])
    resolved = whenResolvedByPython(constructor)
    assert resolved == [
        'def __init__(self, fur: Fur, tail: Tail, claws: Claws):',
        '    self.fur = fur',
        '    self.tail = tail',
        '    self.claws = claws'
    ]


def test_in_Java_FieldDeclaration():
    decl = givenFieldDeclaration('cat')
    resolved = whenResolvedByJava(decl)
    assert resolved == 'public Cat cat;'


def test_in_Python_FieldDeclaration_is_done_in_constructor_so_empty():
    decl = givenFieldDeclaration('cat')
    resolved = whenResolvedByPython(decl)
    assert resolved == ''


def givenFieldDeclaration(name):
    return FieldDeclaration(
        givenUnresolvedVariableName(name=name),
        givenUnresolvedTypeName(name=name)
    )


def givenFieldReference(name):
    return FieldReference(givenUnresolved(UnresolvedVariableName, name))


def givenParameter(name):
    symbol = makeSymbol(name)
    name = UnresolvedVariableName(symbol)
    type = UnresolvedTypeName(symbol)
    param = Parameter(name, type)
    return param


def givenListParameter(name):
    symbol = makeSymbol(name)
    name = UnresolvedListVariableName(symbol)
    type = UnresolvedListTypeName(symbol)
    param = Parameter(name, type)
    return param


def givenSimpleConstructor(name, fields):
    className = givenUnresolvedClassName(name=name)
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
    param = givenUnresolved(UnresolvedVariableName, name)
    return AssignVariableToField(fieldRef, param)


def givenUnresolvedTypeName(name='', givenName='', isTerminal=False):
    return givenUnresolved(of=UnresolvedTypeName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenUnresolvedVariableName(name='', givenName='', isTerminal=False):
    return givenUnresolved(of=UnresolvedVariableName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenUnresolvedClassName(name='', givenName='', isTerminal=False):
    return givenUnresolved(of=UnresolvedClassName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenUnresolvedBaseClassName(name='', givenName='', isTerminal=False):
    return givenUnresolved(of=UnresolvedBaseClassName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenUnresolvedListVariableName(name='', givenName='', isTerminal=False):
    return givenUnresolved(of=UnresolvedListVariableName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenUnresolvedListTypeName(name='', givenName='', isTerminal=False):
    return givenUnresolved(of=UnresolvedListTypeName, name=name, givenName=givenName, isTerminal=isTerminal)


def givenUnresolved(of, name, givenName='', isTerminal=False):
    symbol = makeSymbol(name=name, given=givenName, isTerminal=isTerminal)
    unresolvedName = of(symbol)
    return unresolvedName


def makeSymbol(name=None, given=None, isTerminal=None):
    return Symbol(
        name=name,
        givenName=given,
        isCapture=None,
        isTerminal=isTerminal
    )


def whenResolvedByDefault(unresolved):
    return whenResolve(unresolved, DefaultTranslator())


def whenResolvedByPython(unresolved):
    return whenResolve(unresolved, PythonTranslator())


def whenResolvedByJava(unresolved):
    return whenResolve(unresolved, JavaTranslator())


def whenResolve(unresolved, using):
    return unresolved.to(using)
