import pytest


from plcc.spec.bnfspec import BnfSpec
from plcc.spec.bnfrule import BnfRule
from plcc.spec.symbol import Symbol
from plcc.spec.line import Line
from plcc.spec.parser.bnfparser import BnfParser
from plcc.spec.parser.specreader import SpecReader

from plcc.ast_class_generator.ast import AstClassGenerator

from plcc.code import *


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
    classes = astGenerator.generate(spec)
    assert len(classes) == 1
    c = classes[0]
    assert c.name == ClassName(nonterminal('one'))
    assert c.extends == StrClassName('_Start')


def test_one_rule_with_one_nonterminal(astGenerator):
    spec = givenBnfSpec('<one> ::= <two>')
    classes = astGenerator.generate(spec)
    assert len(classes) == 1
    c = classes[0]

    one = nonterminal('one')
    two = nonterminal('two')
    twoName = VariableName(two)
    twoType = TypeName(two)

    assert c.fields[0] == FieldDeclaration(
        name=twoName,
        type=twoType
    )
    assert c.constructor == Constructor(
        className=ClassName(one),
        parameters=[
            Parameter(
                name=twoName,
                type=twoType
            )
        ],
        assignments=[
            AssignVariableToField(
                lhs=FieldReference(name=twoName),
                rhs=twoName
            )
        ]
    )


def test_one_rule_with_uncaptured_nonterminal(astGenerator):
    spec = givenBnfSpec('<one> ::= <alpha> IGNORE <BRAVO>')
    classes = astGenerator.generate(spec)
    assert len(classes) == 1
    c = classes[0]

    one = nonterminal('one')

    alpha = nonterminal('alpha')
    alphaName = VariableName(alpha)
    alphaType = TypeName(alpha)

    BRAVO = terminal('BRAVO')
    BRAVOName = VariableName(BRAVO)
    BRAVOType = TypeName(BRAVO)

    assert c.fields[0] == FieldDeclaration(
        name=alphaName,
        type=alphaType
    )
    assert c.fields[1] == FieldDeclaration(
        name=BRAVOName,
        type=BRAVOType
    )
    assert c.constructor == Constructor(
        className=ClassName(one),
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
        assignments=[
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
    classes = astGenerator.generate(spec)
    assert len(classes) == 1
    c = classes[0]

    one = nonterminal('one')

    alpha = nonterminal('alpha')
    alphaName = ListVariableName(alpha)
    alphaType = ListTypeName(alpha)

    BRAVO = terminal('BRAVO')
    BRAVOName = ListVariableName(BRAVO)
    BRAVOType = ListTypeName(BRAVO)

    assert c.fields[0] == FieldDeclaration(
        name=alphaName,
        type=alphaType
    )
    assert c.fields[1] == FieldDeclaration(
        name=BRAVOName,
        type=BRAVOType
    )
    assert c.constructor == Constructor(
        className=ClassName(one),
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
        assignments=[
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
    classes = astGenerator.generate(spec)
    assertStartClass(classes[0], nonterminal('one'))
    assertClass(classes[1], nonterminal('two'))


def test_alternative_rules(astGenerator):
    spec = givenBnfSpec('''\
        <firstRuleCannotHaveAlternative> ::= <one>
        <one>:Some ::= <two>
        <one>:None ::=
    ''')
    classes = astGenerator.generate(spec)
    oneSome = nonterminal('one', 'Some')
    oneNone = nonterminal('one', 'None')
    assertBaseClass(classes[0], oneSome)
    assertStartClass(classes[1], nonterminal('firstRuleCannotHaveAlternative'))
    assertSubclass(classes[2], oneSome)
    assertSubclass(classes[3], oneNone)


def assertClass(class_, symbol):
    assert class_.name == ClassName(symbol)
    assert class_.extends is None


def assertBaseClass(class_, symbol):
    assert class_.name == BaseClassName(symbol)
    assert class_.extends is None


def assertStartClass(class_, symbol):
    assert class_.name == ClassName(symbol)
    assert class_.extends == StrClassName(name='_Start')


def assertSubclass(class_, symbol):
    assert class_.name == ClassName(symbol)
    assert class_.extends == BaseClassName(symbol)


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
