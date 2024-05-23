import pytest


from plcc.spec.line import Line
from plcc.spec.bnfrule import BnfRule, Tnt, TntType
from plcc.spec.bnfparser import BnfParser
from plcc.spec.reader import SpecReader


def toRules(string):
    lines = list(readLinesFromString(string))
    parser = BnfParser()
    spec = parser.parseBnfSpec(lines)
    rules = list(spec.getRules())
    return rules


def readLinesFromString(string):
    return SpecReader().readLinesFromString(string)


def test_standard():
    rules = toRules(
        '<one> ::= ONE <two>\n'
        '<two> ::= TWO'
    )
    assert len(rules) == 2
    assert rules == [
        BnfRule(
            line=Line(
                path='',
                number=1,
                string='<one> ::= ONE <two>',
                isInBlock=False
            ),
            lhs=Tnt(type=TntType.NONTERMINAL, name='one', alt='', capture=True),
            op='::=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='ONE', alt='', capture=False),
                Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True)
            ],
            sep=None
        ),
        BnfRule(
            line=Line(
                path='',
                number=2,
                string='<two> ::= TWO',
                isInBlock=False
            ),
            lhs=Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True),
            op='::=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='TWO', alt='', capture=False)
            ],
            sep=None
        )
    ]


def test_repeating():
    rules = toRules(
        '<one> **= ONE <two> +THREE\n'
    )
    assert len(rules) == 1
    assert rules == [
        BnfRule(
            line=Line(
                path='',
                number=1,
                string='<one> **= ONE <two> +THREE',
                isInBlock=False
            ),
            lhs=Tnt(type=TntType.NONTERMINAL, name='one', alt='', capture=True),
            op='**=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='ONE', alt='', capture=False),
                Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True)
            ],
            sep=Tnt(type=TntType.TERMINAL, name='THREE', alt='', capture=False)
        )
    ]

def test_skip_blank_lines_and_comment_lines():
    rules = toRules(
        '    \n'
        '    # a comment to ignore\n'
        '<one> **= ONE <two> +THREE\n'
    )
    assert len(rules) == 1
    assert rules == [
        BnfRule(
            line=Line(
                path='',
                number=3,
                string='<one> **= ONE <two> +THREE',
                isInBlock=False
            ),
            lhs=Tnt(type=TntType.NONTERMINAL, name='one', alt='', capture=True),
            op='**=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='ONE', alt='', capture=False),
                Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True)
            ],
            sep=Tnt(type=TntType.TERMINAL, name='THREE', alt='', capture=False)
        )
    ]
