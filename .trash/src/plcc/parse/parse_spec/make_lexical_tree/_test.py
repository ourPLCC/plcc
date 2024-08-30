from pytest import fixture, mark, raises


from . import make_lexical_tree, LexicalTree, SkipRule, TokenRule
from ...read_sections import Line


def assertParse(given, expect):
    assert make_lexical_tree(given) == expect


def test_None():
    assertParse(None, LexicalTree(rules=[]))


def test_empty():
    assertParse(r'', LexicalTree(rules=[]))


def test_comment():
    assertParse(r'# comment', LexicalTree(rules=[]))


def test_blank_lines():
    given = r'''


    '''
    assertParse(given, LexicalTree(rules=[]))


def test_skip():
    given =r'''

        skip WS '\s'

    '''

    expect = LexicalTree(
        rules=[SkipRule(
            name='WS',
            pattern=r'\s',
            line=Line(
                string=r"        skip WS '\s'",
                number=3,
                file=None
            ))]
    )

    assertParse(given, expect)


def test_token():
    given =r'''

        token WS '\s'

    '''

    expect = LexicalTree(
        rules=[TokenRule(
            name='WS',
            pattern=r'\s',
            line=Line(
                string=r"        token WS '\s'",
                number=3,
                file=None
            ))]
    )

    assertParse(given, expect)



def test_implicit_token():
    given =r'''

        WS '\s'

    '''

    expect = LexicalTree(
        rules=[TokenRule(
            name='WS',
            pattern=r'\s',
            line=Line(
                string=r"        WS '\s'",
                number=3,
                file=None
            ))]
    )

    assertParse(given, expect)



def test_eol_comments():
    given =r'''

        WS ' # \s' # comment

    '''

    expect = LexicalTree(
        rules=[TokenRule(
            name='WS',
            pattern=r' # \s',
            line=Line(
                string=r"        WS ' # \s' # comment",
                number=3,
                file=None
            ))]
    )

    assertParse(given, expect)


def test_integration():
    given =r'''

        skip WS ' # \s' # comment
        token NAME "\w+"

    COMMA ','

    '''

    expect = LexicalTree(
        rules=[
            SkipRule(
                name='WS',
                pattern=' # \\s',
                line=Line(
                    string="        skip WS ' # \\s' # comment",
                    number=3,
                    file=None,
                ),
            ),
            TokenRule(
                name='NAME',
                pattern='\\w+',
                line=Line(
                    string='        token NAME "\\w+"',
                    number=4,
                    file=None,
                ),
            ),
            TokenRule(
                name='COMMA',
                pattern=',',
                line=Line(
                    string="    COMMA ','",
                    number=6,
                    file=None,
                ),
            )
        ]
    )

    assertParse(given, expect)
