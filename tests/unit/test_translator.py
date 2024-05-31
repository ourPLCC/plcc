import pytest


from plcc.spec import bnfrule

from plcc.translator import code
from plcc.translator.java import JavaTranslator
from plcc.translator.python import PythonTranslator


def makeSymbol(name=None, alt=None, isTerminal=None):
    return bnfrule.Symbol(
        name=name,
        alt=alt,
        isCapture=None,
        isTerminal=isTerminal
    )


def test_capitalize_symbol_name_to_make_a_type_name():
    symbol = makeSymbol(name='cat', alt='pet')
    name = code.UnresolvedTypeName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'Cat')


def test_use_provided_name_for_variable_name():
    symbol = makeSymbol(name= 'cat', alt= 'pet')
    name = code.UnresolvedVariableName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'pet')


def test_use_symbol_name_vor_variable_name_if_no_name_provided():
    symbol = makeSymbol(name='cat', alt=None)
    name = code.UnresolvedVariableName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'cat')


def test_type_for_a_terminal_is_Token():
    symbol = makeSymbol(name='cat', alt='pet', isTerminal=True)
    name = code.UnresolvedTypeName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'Token')


def test_the_class_name_of_a_symbol_is_its_name_capitalized():
    symbol = makeSymbol(name='cat', alt=None)
    name = code.UnresolvedClassName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'Cat')


def test_use_provided_name_for_class_name():
    symbol = makeSymbol(name='cat', alt='Pet')
    name = code.UnresolvedClassName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'Pet')


def test_capitalize_symbol_name_to_make_base_class_name():
    symbol = makeSymbol(name='cat', alt='Pet')
    name = code.UnresolvedBaseClassName(symbol)
    assertBothJavaAndPythonResolveNameTo(name, 'Cat')


def assertBothJavaAndPythonResolveNameTo(name, string):
    assert name.to(JavaTranslator()) == string
    assert name.to(PythonTranslator()) == string
