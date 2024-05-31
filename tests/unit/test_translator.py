import pytest


from plcc.spec import bnfrule

from plcc.translator import code
from plcc.translator.java import JavaTranslator
from plcc.translator.python import PythonTranslator


def test_TypeName_resolves_to_capitalized_symbol_name():
    assertResolvesTo(code.UnresolvedTypeName, name='cat', alt='pet', resolvesTo='Cat')


def test_VariableName_resolves_to_symbol_given_name():
    assertResolvesTo(code.UnresolvedVariableName, name='cat', alt='pet', resolvesTo='pet')


def test_VariableName_resolves_to_symbol_name_if_no_given_name():
    assertResolvesTo(code.UnresolvedVariableName, name='cat', alt=None, resolvesTo='cat')


def test_TypeName_resolves_to_Token_for_terminal_symbols():
    assertResolvesTo(code.UnresolvedTypeName, name='cat', alt='pet', isTerminal=True, resolvesTo='Token')


def test_ClassName_resolves_to_symbol_given_name():
    assertResolvesTo(code.UnresolvedClassName, name='cat', alt='Pet', resolvesTo='Pet')


def test_ClassName_resolves_to_capitalized_symbol_name_if_no_given_name():
    assertResolvesTo(code.UnresolvedClassName, name='cat', alt=None, resolvesTo='Cat')


def test_BaseClassName_resolves_to_capitalized_symbol_name():
    assertResolvesTo(code.UnresolvedBaseClassName, name='cat', alt='Pet', resolvesTo='Cat')


def assertResolvesTo(UnresolvedNameType, name=None, alt=None, isTerminal=None, resolvesTo=''):
    symbol = makeSymbol(name=name, alt=alt, isTerminal=isTerminal)
    unresolvedName = UnresolvedNameType(symbol)
    assertBothJavaAndPythonResolveNameTo(unresolvedName, resolvesTo)


def makeSymbol(name=None, alt=None, isTerminal=None):
    return bnfrule.Symbol(
        name=name,
        alt=alt,
        isCapture=None,
        isTerminal=isTerminal
    )


def assertBothJavaAndPythonResolveNameTo(name, string):
    assert name.to(JavaTranslator()) == string
    assert name.to(PythonTranslator()) == string
