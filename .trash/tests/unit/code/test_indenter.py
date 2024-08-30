import pytest


from plcc.code.presenter import Indenter


def test_one_line_string():
    i = Indenter()
    assert i.indent('one') == '    one'


def test_two_line_string():
    i = Indenter()
    assert i.indent('one\ntwo') == '    one\n    two'


def test_blank_lines_not_indented_in_string():
    i = Indenter()
    assert i.indent('one\n\ntwo') == '    one\n\n    two'


def test_one_line_list():
    i = Indenter()
    assert i.indent(['one']) == ['    one']


def test_two_line_list():
    i = Indenter()
    assert i.indent(['one','two']) == ['    one','    two']


def test_blank_lines_not_indented_in_list():
    i = Indenter()
    assert i.indent(['one', '', 'two']) == ['    one', '', '    two']

