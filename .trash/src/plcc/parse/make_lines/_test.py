from pytest import fixture, mark, raises


from . import make_lines, Line


def test_None():
    assert make_lines(None) == []


def test_empty_string():
    assert make_lines('') == []


def test_empty_list():
    assert make_lines([]) == []


def test_no_eol():
    assert make_lines('one') == [Line(string='one', number=1, file=None)]


def test_eol():
    assert make_lines('one\n') == [Line(string='one', number=1, file=None)]


def test_eol_in_list():
    assert make_lines(['one\n']) == [Line(string='one', number=1, file=None)]


def test_many():
    assert make_lines('''
        two
        three
    '''
    ) == [
        Line(string='', number=1, file=None),
        Line(string='        two', number=2, file=None),
        Line(string='        three', number=3, file=None),
        Line(string='    ', number=4, file=None),
    ]

