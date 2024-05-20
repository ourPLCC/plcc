import pytest

from plcc.specfile.line import toLines
from plcc.specfile.bnfparse import BnfParser


def test_standard():
    lines = list(toLines(
        '<one> ::= ONE <two>\n'
        '<two> ::= TWO'
    ))
    assert len(lines) == 2
    rules = BnfParser().parse(lines)
    assert len(rules) == 2
