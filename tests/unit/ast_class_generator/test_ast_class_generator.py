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


def test_one_rule_with_one_nonterminal(astGenerator):
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
            AssignVariableToField(
                lhs=FieldReference(name=twoName),
                rhs=twoName
            )
        ]
    )


def test_one_rule_with_uncaptured_nonterminal(astGenerator):
    spec = givenBnfSpec('<one> ::= <alpha> IGNORE <BRAVO>')
    modules = astGenerator.generate(spec)
    assert len(modules) == 1
    c = modules[0].classes[0]

    one = nonterminal('one')

    alpha = nonterminal('alpha')
    alphaName = UnresolvedVariableName(alpha)
    alphaType = UnresolvedTypeName(alpha)

    BRAVO = terminal('BRAVO')
    BRAVOName = UnresolvedVariableName(BRAVO)
    BRAVOType = UnresolvedTypeName(BRAVO)

    assert c.fields[0] == FieldDeclaration(
        name=alphaName,
        type=alphaType
    )
    assert c.fields[1] == FieldDeclaration(
        name=BRAVOName,
        type=BRAVOType
    )
    assert c.constructor == Constructor(
        className=UnresolvedClassName(one),
        parameters=[
            Parameter(
                name=alphaName,
                type=alphaType
            ),
            Parameter(
                name=BRAVOName,
                type=BRAVOType
            )
        ],
        body=[
            AssignVariableToField(
                lhs=FieldReference(name=alphaName),
                rhs=alphaName
            ),
            AssignVariableToField(
                lhs=FieldReference(name=BRAVOName),
                rhs=BRAVOName
            )
        ]
    )


def test_one_repeating_rule(astGenerator):
    spec = givenBnfSpec('<one> **= <alpha> IGNORE <BRAVO> +IGNORE')
    modules = astGenerator.generate(spec)
    assert len(modules) == 1
    c = modules[0].classes[0]

    one = nonterminal('one')

    alpha = nonterminal('alpha')
    alphaName = UnresolvedListVariableName(alpha)
    alphaType = UnresolvedListTypeName(alpha)

    BRAVO = terminal('BRAVO')
    BRAVOName = UnresolvedListVariableName(BRAVO)
    BRAVOType = UnresolvedListTypeName(BRAVO)

    assert c.fields[0] == FieldDeclaration(
        name=alphaName,
        type=alphaType
    )
    assert c.fields[1] == FieldDeclaration(
        name=BRAVOName,
        type=BRAVOType
    )
    assert c.constructor == Constructor(
        className=UnresolvedClassName(one),
        parameters=[
            Parameter(
                name=alphaName,
                type=alphaType
            ),
            Parameter(
                name=BRAVOName,
                type=BRAVOType
            )
        ],
        body=[
            AssignVariableToField(
                lhs=FieldReference(name=alphaName),
                rhs=alphaName
            ),
            AssignVariableToField(
                lhs=FieldReference(name=BRAVOName),
                rhs=BRAVOName
            )
        ]
    )


def test_multiple_rules(astGenerator):
    spec = givenBnfSpec('''\
        <one> ::= <two>
        <two> ::=
    ''')
    modules = astGenerator.generate(spec)
    assertStartClass(modules[0].classes[0], nonterminal('one'))
    assertClass(modules[1].classes[0], nonterminal('two'))


def test_alternative_rules(astGenerator):
    spec = givenBnfSpec('''\
        <firstRuleCannotHaveAlternative> ::= <one>
        <one>:Some ::= <two>
        <one>:None ::=
    ''')
    modules = astGenerator.generate(spec)
    oneSome = nonterminal('one', 'Some')
    oneNone = nonterminal('one', 'None')
    assertBaseClass(modules[0].classes[0], oneSome)
    assertStartClass(modules[1].classes[0], nonterminal('firstRuleCannotHaveAlternative'))
    assertSubclass(modules[2].classes[0], oneSome)
    assertSubclass(modules[3].classes[0], oneNone)


def assertClass(class_, symbol):
    assert class_.name == UnresolvedClassName(symbol)
    assert class_.extends is None


def assertBaseClass(class_, symbol):
    assert class_.name == UnresolvedBaseClassName(symbol)
    assert class_.extends is None


def assertStartClass(class_, symbol):
    assert class_.name == UnresolvedClassName(symbol)
    assert class_.extends == ClassName(name='_Start')


def assertSubclass(class_, symbol):
    assert class_.name == UnresolvedClassName(symbol)
    assert class_.extends == UnresolvedBaseClassName(symbol)


def nonterminal(name, given=''):
    return Symbol(
        name=name,
        givenName=given,
        isCapture=True,
        isTerminal=False
    )


def terminal(name):
    return Symbol(
        name=name,
        givenName='',
        isCapture=True,
        isTerminal=True
    )
