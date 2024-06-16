from pathlib import Path


from pytest import fixture, raises, mark


from . import LineReader, Line, toLines


@fixture
def reader():
    return LineReader()


@fixture
def nonexistent():
    return Path('/File')


@fixture
def empty(fs, nonexistent):
    fs.create_file(nonexistent)
    return nonexistent


@fixture
def unreadable(fs, empty):
    fs.chmod(empty, 0o000)
    return empty


@fixture
def file(empty):
    return empty


def write(empty, contents):
    with empty.open('w') as f:
        f.write(contents)
    return empty


def test_nonexistent_file(reader, nonexistent):
    with raises(FileNotFoundError):
        reader.read(nonexistent)


def test_unreadable_file(reader, unreadable):
    with raises(PermissionError):
        reader.read(unreadable)


def test_empty_file(reader, empty):
    assert reader.read(empty) == []


def test_one_line(reader, file):
    write(file, 'one')
    lines = reader.read(file)
    assert len(lines) == 1
    assert lines[0].string == 'one'
    assert lines[0].number == 1
    assert lines[0].file == str(file.resolve())


def test_one_line_with_newline(reader, file):
    write(file, 'one\n')
    path = str(file.resolve())
    assert reader.read(file) == toLines(['one'], path)


def test_many_lines(reader, file):
    write(file, 'one\ntwo\nthree')
    path = str(file.resolve())
    assert reader.read(file) == toLines(['one', 'two', 'three'], path)
