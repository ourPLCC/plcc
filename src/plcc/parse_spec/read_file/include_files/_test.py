from pytest import raises, fixture, mark


from ..read_lines import LineReader, Line
from ..mark_blocks import BlockMarkingLineReader
from ..mark_blocks import isInBlock, markLineInBlock
from . import IncludeReader, CircularIncludeError


def test_include(fs):
    fs.create_file('/a', contents='''\
one
%include /b
two
''')

    fs.create_file('/b', contents='''\
alpha
bravo
''')

    reader = IncludeReader(LineReader)
    lines = reader.read('/a')
    assert lines[0] == Line('one', 1, '/a')
    assert lines[1] == Line('alpha', 1, '/b')
    assert lines[2] == Line('bravo', 2, '/b')
    assert lines[3] == Line('two', 3, '/a')


def test_detect_cycle(fs):
    fs.create_file('/a', contents='''\
one
%include /b
two
''')

    fs.create_file('/b', contents='''\
alpha
%include /a
bravo
''')

    reader = IncludeReader()
    with raises(CircularIncludeError) as info:
        lines = reader.read('/a')
    e = info.value
    assert e.line == Line('%include /a', 2, '/b')


def test_relative_include(fs):
    fs.create_file('/a', contents='''\
%include /b
''')

    fs.create_file('/b', contents='''\
%include f/c
''')

    fs.create_file('/f/c', contents='''\
%include g/d
''')

    fs.create_file('/f/g/d', contents='''\
got it
''')

    reader = IncludeReader()
    assert reader.read('/a')[0].string == 'got it'


def test_ignore_in_block(fs):
    fs.create_file('/a', contents='''\
one
%%%
%include /b
%%%
two
''')

    fs.create_file('/b', contents='''\
alpha
bravo
''')

    reader = IncludeReader()
    lines = reader.read('/a')
    assert lines[0] == Line('one', 1, '/a')
    assert lines[1] == Line('%%%', 2, '/a')
    assert lines[2] == markLineInBlock(Line('%include /b', 3, '/a'))
    assert lines[3] == Line('%%%', 4, '/a')
    assert lines[4] == Line('two', 5, '/a')
