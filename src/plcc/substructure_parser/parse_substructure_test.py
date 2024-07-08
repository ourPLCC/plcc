from pytest import fixture, raises, mark


from .parse_substructure import parse_substructure
from .parse_lines import Line
from .parse_blocks import Block
from .parse_dividers import Divider
from .parse_includes import Include


def test_():
    assert list(parse_substructure('''\
one
%
two
% java
%include /A.java
% python
%include /B.py
% c++
%%%
%include nope
% nope
%%%
''')) == [
    Line('one', 1, None),
    Divider(Line('%', 2, None)),
    Line('two', 3, None),
    Divider(Line('% java', 4, None)),
    Include(file='/A.java', line=Line('%include /A.java', 5, None)),
    Divider(Line('% python', 6, None)),
    Include(file='/B.py', line=Line('%include /B.py', 7, None)),
    Divider(Line('% c++', 8, None)),
    Block([
        Line('%%%', 9, None),
        Line('%include nope', 10, None),
        Line('% nope', 11, None),
        Line('%%%', 12, None)
    ])
]
