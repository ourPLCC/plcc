import pytest

from plcc.specfile.line import toLines
from plcc.specfile.bnfparse import BnfParser, BnfRule, Tnt


def test_standard():
    lines = list(toLines(
        '<one> ::= ONE <two>\n'
        '<two> ::= TWO'
    ))
    rules = list(BnfParser().parse(lines))
    assert len(rules) == 2
    assert rules == [
        BnfRule(
            lhs=Tnt(type='nonterminal', name='one', alt='', capture=True),
            op='::=',
            tnts=[
                Tnt(type='terminal', name='ONE', alt='', capture=False),
                Tnt(type='nonterminal', name='two', alt='', capture=True)
            ],
            sep=None
        ),
        BnfRule(
            lhs=Tnt(type='nonterminal', name='two', alt='', capture=True),
            op='::=',
            tnts=[
                Tnt(type='terminal', name='TWO', alt='', capture=False)
            ],
            sep=None
        )
    ]

def test_repeating():
    lines = list(toLines(
        '<one> **= ONE <two> +THREE\n'
    ))
    rules = list(BnfParser().parse(lines))
    assert len(rules) == 1
    assert rules == [
        BnfRule(
            lhs=Tnt(type='nonterminal', name='one', alt='', capture=True),
            op='**=',
            tnts=[
                Tnt(type='terminal', name='ONE', alt='', capture=False),
                Tnt(type='nonterminal', name='two', alt='', capture=True)
            ],
            sep=Tnt(type='terminal', name='THREE', alt='', capture=False)
        )
    ]

def test_skip_blank_lines_and_comment_lines():

    lines = list(toLines(
        '    \n'
        '    # a comment to ignore\n'
        '<one> **= ONE <two> +THREE\n'
    ))
    rules = list(BnfParser().parse(lines))
    assert len(rules) == 1
    assert rules == [
        BnfRule(
            lhs=Tnt(type='nonterminal', name='one', alt='', capture=True),
            op='**=',
            tnts=[
                Tnt(type='terminal', name='ONE', alt='', capture=False),
                Tnt(type='nonterminal', name='two', alt='', capture=True)
            ],
            sep=Tnt(type='terminal', name='THREE', alt='', capture=False)
        )
    ]
