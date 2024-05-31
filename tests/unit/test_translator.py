import pytest


from plcc.spec.symbol import Symbol

from plcc.translator import code
from plcc.translator.java import JavaTranslator
from plcc.translator.python import PythonTranslator


def test_variable_declaration():
    s = Symbol(name='x')
    v = code.UnresolvedVariableName(s)
    t = code.UnresolvedTypeName(s)
    decl = code.VariableDeclaration(name=v, type=t)
    assert decl.to(JavaTranslator()) == 'X x = null;'
    assert decl.to(PythonTranslator()) == 'x = None'
