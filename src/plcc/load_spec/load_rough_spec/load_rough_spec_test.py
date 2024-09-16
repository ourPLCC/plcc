from pytest import raises, mark, fixture

from .parse_lines import Line
from .parse_blocks import Block
from .parse_dividers import Divider
from .load_rough_spec import load_rough_spec
from .split_rough_spec import RoughSpec, split_rough_spec


def test_load_rough_spec(fs):
    fs.create_file('A.java', contents='hi in java')
    fs.create_file('B.py', contents='hi in python')
    fs.create_file('test.py', contents='''\
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
''')
    assert load_rough_spec('test.py') == split_rough_spec([
        makeLine('one', 1, 'test.py'),
        makeDivider('%', 2, 'test.py'),
        makeLine('two', 3, 'test.py'),
        makeDivider('% java', 4, 'test.py'),
        makeLine('hi in java', 1, '/A.java'),
        makeDivider('% python', 6, 'test.py'),
        makeLine('hi in python', 1, '/B.py'),
        makeDivider('% c++', 8, 'test.py'),
        makeBlock('''
            %%%
            %include nope
            % nope
            %%%
        ''', 9, 12, 'test.py')
    ])


def makeBlockList(string):
    lines = [makeLine(s) for s in string.strip().split('\n')]


def makeLine(string, lineNumber=None, file=None):
    return Line(string, lineNumber, file)


def makeDivider(string, lineNumber=None, file=None):
    return Divider(makeLine(string, lineNumber, file))


def makeBlock(string, startLine, endLine, file=None):
    return Block([makeLine(s.strip(), num, file) for s, num in zip(string.strip().split('\n'), range(startLine, endLine + 1))])

