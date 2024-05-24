import pytest


from plcc.spec.line import Line
from plcc.spec.bnfrule import BnfRule, Tnt
from plcc.spec.bnfparser import BnfParser
from plcc.spec.specreader import SpecReader


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
                isInCodeBlock=False
            ),
            lhs=Tnt(isTerminal=False, name='one', alt='', isCapture=True),
            isRepeating=False,
            tnts=[
                Tnt(isTerminal=True, name='ONE', alt='', isCapture=False),
                Tnt(isTerminal=False, name='two', alt='', isCapture=True)
            ],
            sep=None
        ),
        BnfRule(
            line=Line(
                path='',
                number=2,
                string='<two> ::= TWO',
                isInCodeBlock=False
            ),
            lhs=Tnt(isTerminal=False, name='two', alt='', isCapture=True),
            isRepeating=False,
            tnts=[
                Tnt(isTerminal=True, name='TWO', alt='', isCapture=False)
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
                isInCodeBlock=False
            ),
            lhs=Tnt(isTerminal=False, name='one', alt='', isCapture=True),
            isRepeating=True,
            tnts=[
                Tnt(isTerminal=True, name='ONE', alt='', isCapture=False),
                Tnt(isTerminal=False, name='two', alt='', isCapture=True)
            ],
            sep=Tnt(isTerminal=True, name='THREE', alt='', isCapture=False)
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
                isInCodeBlock=False
            ),
            lhs=Tnt(isTerminal=False, name='one', alt='', isCapture=True),
            isRepeating=True,
            tnts=[
                Tnt(isTerminal=True, name='ONE', alt='', isCapture=False),
                Tnt(isTerminal=False, name='two', alt='', isCapture=True)
            ],
            sep=Tnt(isTerminal=True, name='THREE', alt='', isCapture=False)
        )
    ]
