from pathlib import Path


from pytest import fixture, mark, raises


from . import FileReader, Line, LineInBlock, isInBlock, CircularIncludeError


@fixture
def reader():
    return FileReader()


@fixture
def nonexistent():
    return Path('/a_test_file')


@fixture
def empty(fs, nonexistent):
    fs.create_file(nonexistent)
    return nonexistent


@fixture
def unreadable(fs, empty):
    fs.chmod(empty, 0o000)
    return empty


def givenFile(fs, pathString, contents):
    fs.create_file(pathString, contents=contents)


def test_nonexistent(reader, nonexistent):
    with raises(FileNotFoundError):
        reader.read(nonexistent)


def test_unreadable(reader, unreadable):
    with raises(PermissionError):
        reader.read(unreadable)


def test_empty(reader, empty):
    assert reader.read(empty) == []


def test_read_one_line_without_newline(fs, reader):
    givenFile(fs, '/a', 'one')
    assert reader.read('/a') == [ Line('one', 1, '/a') ]


def test_read_one_line(fs, reader):
    givenFile(fs, '/a', 'one\n')
    assert reader.read('/a') == [ Line('one', 1, '/a') ]


def test_read_many_lines(fs, reader):
    givenFile(fs, '/a', '''\
one
two
three
''')
    assert reader.read('/a') == [
        Line('one', 1, '/a'),
        Line('two', 2, '/a'),
        Line('three', 3, '/a'),
    ]


def test_code_blocks(fs, reader):
    givenFile(fs, '/a', '''\
one
%%%
two
%%%
three
''')
    lines = reader.read('/a')
    assert lines == [
        Line('one', 1, '/a'),
        Line('%%%', 2, '/a'),
        LineInBlock('two', 3, '/a'),
        Line('%%%', 4, '/a'),
        Line('three', 5, '/a'),
    ]

    assert isInBlock(lines[2])
    assert lines[2].isInBlock

    assert not isInBlock(lines[1])
    with raises(AttributeError):
        lines[1].isInBlock


def test_code_blocks_alternate_syntax(fs, reader):
    givenFile(fs, '/a', '''\
one
%%{
two
%%}
three
''')
    lines = reader.read('/a')
    assert isInBlock(lines[2])
    assert not isInBlock(lines[1])


def test_include(fs, reader):
    givenFile(fs, '/a', contents='''\
alpha
%include /b
charlie
''')
    givenFile(fs, '/b', contents='bravo')
    lines = reader.read('/a')
    assert lines == [
        Line('alpha', 1, '/a'),
        Line('bravo', 1, '/b'),
        Line('charlie', 3, '/a')
    ]


def test_detects_circular_includes(fs, reader):
    givenFile(fs, '/a', contents='%include /b')
    givenFile(fs, '/b', contents='%include /a')
    with raises(CircularIncludeError) as info:
        lines = reader.read('/a')
    exception = info.value
    assert exception.line == Line('%include /a', 1, '/b')


def test_relative_includes(fs, reader):
    givenFile(fs, '/f/a', contents='%include ../g/b')
    givenFile(fs, '/g/b', contents='%include h/c')
    givenFile(fs, '/g/h/c', contents='got it')
    assert reader.read('/f/a') == [ Line('got it', 1, '/g/h/c') ]
