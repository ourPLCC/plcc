import pytest


from plcc.spec.bnfspec import BnfSpec
from plcc.spec.bnfrule import BnfRule
from plcc.spec.symbol import Symbol
from plcc.spec.parser.bnfparser import BnfParser
from plcc.spec.parser.specreader import SpecReader


from plcc.code.generator.ast import AstGenerator
from plcc.code.module import Module
from plcc.code.class_ import Class
from plcc.code.names import UnresolvedClassName
from plcc.code.names import ClassName


@pytest.fixture
def astGenerator():
    return AstGenerator()


def givenBnfSpec(string):
    p = BnfParser()
    r = SpecReader()
    lines = r.readLinesFromString(string)
    rules = list(p.parseBnfRules(lines))
    spec = BnfSpec(rules)
    return spec


def test_generate_empty_returns_empty(astGenerator):
    spec = givenBnfSpec('')
    assert astGenerator.generate(spec) == []


def test_single_empty_bnf_rule_returns_one_class(astGenerator):
    spec = givenBnfSpec('<one> ::=')
    modules = astGenerator.generate(spec)
    assert len(modules) == 1
    assert isinstance(modules[0], Module)
    assert isinstance(modules[0].classes[0], Class)
    assert modules[0].classes[0].name == UnresolvedClassName(Symbol(
        name='one',
        givenName='',
        isCapture=True,
        isTerminal=False
    ))
    assert modules[0].classes[0].extends == ClassName('_Start')
