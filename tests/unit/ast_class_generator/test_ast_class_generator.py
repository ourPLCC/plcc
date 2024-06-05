import pytest


from plcc.spec.bnfspec import BnfSpec
from plcc.spec.bnfrule import BnfRule
from plcc.spec.symbol import Symbol
from plcc.spec.line import Line
from plcc.spec.parser.bnfparser import BnfParser
from plcc.spec.parser.specreader import SpecReader

from plcc.ast_class_generator.ast import AstClassGenerator

from plcc.code.structures import *


@pytest.fixture
def astGenerator():
    return AstClassGenerator()


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
    c = modules[0].classes[0]
    assert c.name == UnresolvedClassName(nonterminal('one'))
    assert c.extends == ClassName('_Start')


def test_one_rhs_nonterminal(astGenerator):
    spec = givenBnfSpec('<one> ::= <two>')
    modules = astGenerator.generate(spec)
    assert len(modules) == 1
    c = modules[0].classes[0]

    one = nonterminal('one')
    two = nonterminal('two')
    twoName = UnresolvedVariableName(two)
    twoType = UnresolvedTypeName(two)

    assert c.fields[0] == FieldDeclaration(
        name=twoName,
        type=twoType
    )
    assert c.constructor == Constructor(
        className=UnresolvedClassName(one),
        parameters=[
            Parameter(
                name=twoName,
                type=twoType
            )
        ],
        body=[
            FieldInitialization(
                field=FieldReference(name=twoName),
                parameter=twoName
            )
        ]
    )


def nonterminal(name):
    return Symbol(
        name=name,
        givenName='',
        isCapture=True,
        isTerminal=False
    )
