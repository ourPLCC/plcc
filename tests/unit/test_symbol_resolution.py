import pytest


from plcc.spec import bnfrule

from plcc.translator import code
from plcc.translator.java import JavaTranslator
from plcc.translator.python import PythonTranslator


def test_TypeName_resolves_to_capitalized_symbol_name():
    assertResolvesTo(code.UnresolvedTypeName, name='cat', givenName='pet', resolvesTo='Cat')


def test_VariableName_resolves_to_symbol_given_name():
    assertResolvesTo(code.UnresolvedVariableName, name='cat', givenName='pet', resolvesTo='pet')


def test_VariableName_resolves_to_symbol_name_if_no_given_name():
    assertResolvesTo(code.UnresolvedVariableName, name='cat', givenName=None, resolvesTo='cat')


def test_TypeName_resolves_to_Token_for_terminal_symbols():
    assertResolvesTo(code.UnresolvedTypeName, name='cat', givenName='pet', isTerminal=True, resolvesTo='Token')


def test_ClassName_resolves_to_symbol_given_name():
    assertResolvesTo(code.UnresolvedClassName, name='cat', givenName='Pet', resolvesTo='Pet')


def test_ClassName_resolves_to_capitalized_symbol_name_if_no_given_name():
    assertResolvesTo(code.UnresolvedClassName, name='cat', givenName=None, resolvesTo='Cat')


def test_BaseClassName_resolves_to_capitalized_symbol_name():
    assertResolvesTo(code.UnresolvedBaseClassName, name='cat', givenName='Pet', resolvesTo='Cat')


def assertResolvesTo(UnresolvedNameType, name=None, givenName=None, isTerminal=None, resolvesTo=''):
    symbol = makeSymbol(name=name, given=givenName, isTerminal=isTerminal)
    unresolvedName = UnresolvedNameType(symbol)
    assertBothJavaAndPythonResolveNameTo(unresolvedName, resolvesTo)


def makeSymbol(name=None, given=None, isTerminal=None):
    return bnfrule.Symbol(
        name=name,
        givenName=given,
        isCapture=None,
        isTerminal=isTerminal
    )


def assertBothJavaAndPythonResolveNameTo(name, string):
    assert name.to(JavaTranslator()) == string
    assert name.to(PythonTranslator()) == string
