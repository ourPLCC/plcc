from pytest import raises, mark, fixture


from .parse_lines import parse_lines, Line


def test_None_yields_nothing():
    assert list(parse_lines(None)) == []


def test_empty_yields_nothing():
    assert list(parse_lines('')) == []


def test_eol_yields_single_empty_line():
    assert list(parse_lines('\n')) == [Line('', 1, None)]


def test_one_line_without_eol_yields_single_line():
    assert list(parse_lines('one')) == [Line('one', 1, None)]


def test_one_line_with_eol_yields_single_line():
    assert list(parse_lines('one\n')) == [Line('one', 1, None)]


def test_multiple_lines():
    assert list(parse_lines('one\ntwo')) == [Line('one', 1, None), Line('two', 2, None)]


def test_set_start_of_numbering():
    assert list(parse_lines('one\ntwo', start=3)) == [Line('one', 3, None), Line('two', 4, None)]


def test_set_file():
    assert list(parse_lines('one\ntwo', file='/f')) == [Line('one', 1, '/f'), Line('two', 2, '/f')]
