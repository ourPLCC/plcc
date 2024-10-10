from pytest import fixture, raises, mark


from .parse_rough import parse_rough
from .parse_lines import Line
from .parse_blocks import Block
from .parse_dividers import Divider
from .parse_includes import Include


def test_():
    assert list(parse_rough('''\
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
    Divider(tool='Java', language='Java', line=Line('%', 2, None)),
    Line('two', 3, None),
    Divider(tool='java', language='java', line=Line('% java', 4, None)),
    Include(file='/A.java', line=Line('%include /A.java', 5, None)),
    Divider(tool='python', language='python', line=Line('% python', 6, None)),
    Include(file='/B.py', line=Line('%include /B.py', 7, None)),
    Divider(tool='c++', language='c++', line=Line('% c++', 8, None)),
    Block([
        Line('%%%', 9, None),
        Line('%include nope', 10, None),
        Line('% nope', 11, None),
        Line('%%%', 12, None)
    ])
]
