import pytest

from plcc.specfile.bnfrule import BnfRule, Tnt, TntType
from plcc.specfile.bnfparser import BnfParser
from plcc.specfile.reader import SpecFileReader


def readLinesFromString(string):
    return SpecFileReader().readLinesFromString(string)


def test_standard():
    lines = list(readLinesFromString(
        '<one> ::= ONE <two>\n'
        '<two> ::= TWO'
    ))
    rules = list(BnfParser().parse(lines))
    assert len(rules) == 2
    assert rules == [
        BnfRule(
            lhs=Tnt(type=TntType.NONTERMINAL, name='one', alt='', capture=True),
            op='::=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='ONE', alt='', capture=False),
                Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True)
            ],
            sep=None
        ),
        BnfRule(
            lhs=Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True),
            op='::=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='TWO', alt='', capture=False)
            ],
            sep=None
        )
    ]


def test_repeating():
    lines = list(readLinesFromString(
        '<one> **= ONE <two> +THREE\n'
    ))
    rules = list(BnfParser().parse(lines))
    assert len(rules) == 1
    assert rules == [
        BnfRule(
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
    lines = list(readLinesFromString('    \n'
        '    # a comment to ignore\n'
        '<one> **= ONE <two> +THREE\n'
    ))
    rules = list(BnfParser().parse(lines))
    assert len(rules) == 1
    assert rules == [
        BnfRule(
            lhs=Tnt(type=TntType.NONTERMINAL, name='one', alt='', capture=True),
            op='**=',
            tnts=[
                Tnt(type=TntType.TERMINAL, name='ONE', alt='', capture=False),
                Tnt(type=TntType.NONTERMINAL, name='two', alt='', capture=True)
            ],
            sep=Tnt(type=TntType.TERMINAL, name='THREE', alt='', capture=False)
        )
    ]
