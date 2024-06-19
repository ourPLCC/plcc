from pytest import fixture, mark, raises


from . import parse
from . import SyntacticTree
from . import Defined
from . import Captured
from . import Uncaptured
from . import Nonterminal
from . import RepeatingRule
from . import StandardRule
from . import SyntacticTree
from . import Terminal

from ...read_sections import Line


def assertParse(given, expect):
    assert parse(given) == expect


@mark.focus
def test_None():
    assertParse(None, SyntacticTree(rules=[]))


@mark.focus
def test_empty():
    assertParse(r'', SyntacticTree(rules=[]))


@mark.focus
def test_comment():
    assertParse(r'# comment', SyntacticTree(rules=[]))


@mark.focus
def test_blank_lines():
    given = r'''


    '''
    assertParse(given, SyntacticTree(rules=[]))


@mark.focus
def test_standard():
    given =r'''

        <one> ::=

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        'one'
                    ),
                    disambiguation=None,
                    line=Line(
                        string=r'        <one> ::=',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[]
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_standard_disambiguation():
    given =r'''

        <one>hi ::=

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        'one'
                    ),
                    disambiguation='hi',
                    line=Line(
                        string=r'        <one>hi ::=',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[]
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_standard_colon_disambiguation():
    given =r'''

        <one>:hi ::=

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        'one'
                    ),
                    disambiguation='hi',
                    line=Line(
                        string=r'        <one>:hi ::=',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[]
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_standard_terminal():
    given =r'''

        <one> ::= HI

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        name='one'
                    ),
                    disambiguation=None,
                    line=Line(
                        string=r'        <one> ::= HI',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[
                    Uncaptured(
                        symbol=Terminal(
                            name='HI'
                        ),
                        line=Line(
                            string=r'        <one> ::= HI',
                            number=3,
                            file=None,
                        ),
                        column=19
                    )
                ]
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_standard_captured_terminal():
    given =r'''

        <one> ::= <HI>

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        name='one'
                    ),
                    disambiguation=None,
                    line=Line(
                        string=r'        <one> ::= <HI>',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[
                    Captured(
                        symbol=Terminal(
                            name='HI'
                        ),
                        disambiguation=None,
                        line=Line(
                            string=r'        <one> ::= <HI>',
                            number=3,
                            file=None,
                        ),
                        column=19
                    )
                ]
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_standard_nonterminal():
    given =r'''

        <one> ::= <hi>

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        name='one'
                    ),
                    disambiguation=None,
                    line=Line(
                        string=r'        <one> ::= <hi>',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[
                    Captured(
                        symbol=Nonterminal(
                            name='hi'
                        ),
                        disambiguation=None,
                        line=Line(
                            string=r'        <one> ::= <hi>',
                            number=3,
                            file=None,
                        ),
                        column=19
                    )
                ]
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_standard_integration():
    given =r'''

        <one>Two ::= <hi> HI <YO>:greet

    '''

    expect = SyntacticTree(
        rules=[
            StandardRule(
                defined=Defined(
                    symbol=Nonterminal(
                        name='one'
                    ),
                    disambiguation='Two',
                    line=Line(
                        string=r'        <one>Two ::= <hi> HI <YO>:greet',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[
                    Captured(
                        symbol=Nonterminal(
                            name='hi'
                        ),
                        disambiguation=None,
                        line=Line(
                            string=r'        <one>Two ::= <hi> HI <YO>:greet',
                            number=3,
                            file=None,
                        ),
                        column=22
                    ),
                    Uncaptured(
                        symbol=Terminal(
                            name='HI'
                        ),
                        line=Line(
                            string=r'        <one>Two ::= <hi> HI <YO>:greet',
                            number=3,
                            file=None,
                        ),
                        column=27
                    ),
                    Captured(
                        symbol=Terminal(
                            name='YO'
                        ),
                        disambiguation='greet',
                        line=Line(
                            string=r'        <one>Two ::= <hi> HI <YO>:greet',
                            number=3,
                            file=None,
                        ),
                        column=30
                    )

                ]
            )
        ]
    )

    assertParse(given, expect)



@mark.focus
def test_repeating_empty():
    given =r'''

        <one> **=

    '''

    expect = SyntacticTree(
        rules=[
            RepeatingRule(
                defined=Defined(
                    symbol=Nonterminal(
                        name='one'
                    ),
                    disambiguation=None,
                    line=Line(
                        string=r'        <one> **=',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[
                ],
                separator=None
            )
        ]
    )

    assertParse(given, expect)


@mark.focus
def test_repeating_separator():
    given =r'''

        <one> **= +SEP

    '''

    expect = SyntacticTree(
        rules=[
            RepeatingRule(
                defined=Defined(
                    symbol=Nonterminal(
                        name='one'
                    ),
                    disambiguation=None,
                    line=Line(
                        string=r'        <one> **= +SEP',
                        number=3,
                        file=None,
                    ),
                    column=9
                ),
                symbols=[
                ],
                separator=Uncaptured(
                    symbol=Terminal(
                        name='SEP'
                    ),
                    line=Line(
                        string=r'        <one> **= +SEP',
                        number=3,
                        file=None,
                    ),
                    column=19
                )
            )
        ]
    )

    assertParse(given, expect)
