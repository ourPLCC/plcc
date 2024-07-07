from pytest import fixture, raises, mark
import pyfakefs


from .parse_substructure import parse_substructure
from .parse_lines import Line
from .parse_blocks import Block
from .parse_dividers import Divider


def test_(fs):
    fs.create_file('/A.java', contents='A')
    fs.create_file('/B.py', contents='B')

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
    Line('A', 1, '/A.java'),
    Divider(Line('% python', 6, None)),
    Line('B', 1, '/B.py'),
    Divider(Line('% c++', 8, None)),
    Block([
        Line('%%%', 9, None),
        Line('%include nope', 10, None),
        Line('% nope', 11, None),
        Line('%%%', 12, None)
    ])
]
