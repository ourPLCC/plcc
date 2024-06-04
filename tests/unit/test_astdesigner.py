import pytest


from plcc.code.generator.ast import AstDesigner
from plcc.spec.bnfspec import BnfSpec
from plcc.spec.bnfrule import BnfRule
from plcc.spec.symbol import Symbol
from plcc.spec.parser.bnfparser import BnfParser
from plcc.spec.parser.specreader import SpecReader
from plcc.code.module import Module


@pytest.fixture
def ast_designer():
    return AstDesigner()


def givenBnfSpec(string):
    p = BnfParser()
    r = SpecReader()
    lines = r.readLinesFromString(string)
    rules = list(p.parseBnfRules(lines))
    spec = BnfSpec(rules)
    return spec


def test_design_empty_returns_empty(ast_designer):
    spec = givenBnfSpec('')
    assert ast_designer.design(spec) == []


def test_single_empty_bnf_rule_returns_one_class(ast_designer):
    spec = givenBnfSpec('<one> ::=')
    astClassFiles = ast_designer.design(spec)
    assert len(astClassFiles) == 1
    assert isinstance(astClassFiles[0], Module)

