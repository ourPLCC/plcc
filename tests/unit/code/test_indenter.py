import pytest


from plcc.code.presenter import Indenter


@pytest.mark.focus
def test_one_line_string():
    i = Indenter()
    assert i.indent('one') == '    one'


@pytest.mark.focus
def test_two_line_string():
    i = Indenter()
    assert i.indent('one\ntwo') == '    one\n    two'


@pytest.mark.focus
def test_blank_lines_not_indented_in_string():
    i = Indenter()
    assert i.indent('one\n\ntwo') == '    one\n\n    two'


@pytest.mark.focus
def test_one_line_list():
    i = Indenter()
    assert i.indent(['one']) == ['    one']


@pytest.mark.focus
def test_two_line_list():
    i = Indenter()
    assert i.indent(['one','two']) == ['    one','    two']


@pytest.mark.focus
def test_blank_lines_not_indented_in_list():
    i = Indenter()
    assert i.indent(['one', '', 'two']) == ['    one', '', '    two']

