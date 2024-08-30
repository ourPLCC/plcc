import pytest


from plcc.spec.line import Line
from plcc.spec.bnfrule import BnfRule, Symbol
from plcc.spec.parser.bnfparser import BnfParser
from plcc.spec.parser.specreader import SpecReader


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
            leftHandSymbol=Symbol(isTerminal=False, name='one', givenName='', isCapture=True),
            isRepeating=False,
            rightHandSymbols=[
                Symbol(isTerminal=True, name='ONE', givenName='', isCapture=False),
                Symbol(isTerminal=False, name='two', givenName='', isCapture=True)
            ],
            separator=None
        ),
        BnfRule(
            line=Line(
                path='',
                number=2,
                string='<two> ::= TWO',
                isInCodeBlock=False
            ),
            leftHandSymbol=Symbol(isTerminal=False, name='two', givenName='', isCapture=True),
            isRepeating=False,
            rightHandSymbols=[
                Symbol(isTerminal=True, name='TWO', givenName='', isCapture=False)
            ],
            separator=None
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
            leftHandSymbol=Symbol(isTerminal=False, name='one', givenName='', isCapture=True),
            isRepeating=True,
            rightHandSymbols=[
                Symbol(isTerminal=True, name='ONE', givenName='', isCapture=False),
                Symbol(isTerminal=False, name='two', givenName='', isCapture=True)
            ],
            separator=Symbol(isTerminal=True, name='THREE', givenName='', isCapture=False)
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
            leftHandSymbol=Symbol(isTerminal=False, name='one', givenName='', isCapture=True),
            isRepeating=True,
            rightHandSymbols=[
                Symbol(isTerminal=True, name='ONE', givenName='', isCapture=False),
                Symbol(isTerminal=False, name='two', givenName='', isCapture=True)
            ],
            separator=Symbol(isTerminal=True, name='THREE', givenName='', isCapture=False)
        )
    ]
