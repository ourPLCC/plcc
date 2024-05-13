import pytest


from plcc.specfiles import default_specfile, CircularIncludeException


def test_path_is_None():
    with pytest.raises(TypeError):
        default_specfile(None)


def test_path_is_empty():
    with pytest.raises(ValueError):
        default_specfile('    ')


def test_missing_file(fs):
    file = default_specfile('missing_file')
    with pytest.raises(FileNotFoundError):
        next(file)


def test_empty_file(fs):
    fs.create_file('/f', contents='')
    file = default_specfile('/f')
    with pytest.raises(StopIteration):
        next(file)


def test_single_line_no_line_ending(fs):
    fs.create_file('/f', contents='a')
    file = default_specfile('/f')
    line = next(file)
    assert line.string == 'a'
    with pytest.raises(StopIteration):
        next(file)


def test_single_line(fs):
    fs.create_file('/f', contents='a\n')
    file = default_specfile('/f')
    line = next(file)
    assert line.string == 'a'
    with pytest.raises(StopIteration):
        next(file)


def test_many_lines(fs):
    fs.create_file('/f', contents='a\nb\nc\n')
    file = default_specfile('/f')
    line = next(file)
    assert line.string == 'a'
    line = next(file)
    assert line.string == 'b'
    line = next(file)
    assert line.string == 'c'
    with pytest.raises(StopIteration):
        next(file)


def test_block_marking(fs):
    fs.create_file('/f', contents='''\
not in block
%%%
in block
this too
%%%
not in block
''')
    file = default_specfile('/f')
    line = next(file)
    assert line.string == 'not in block'
    assert not line.isInBlock
    line = next(file)
    assert line.string == '%%%' and not line.isInBlock
    line = next(file)
    assert line.string == 'in block' and line.isInBlock
    line = next(file)
    assert line.string == 'this too' and line.isInBlock
    line = next(file)
    assert line.string == '%%%' and not line.isInBlock
    line = next(file)
    assert line.string == 'not in block' and not line.isInBlock


def test_includes(fs):
    fs.create_file('/f', contents='''\
a
%include /g
b
%include /g
c
''')

    fs.create_file('/g', contents='''\
1
2
''')

    file = default_specfile('/f')

    line = next(file)
    assert line.string == 'a' and line.path == '/f' and line.number == 1
    line = next(file)
    assert line.string == '1' and line.path == '/g' and line.number == 1
    line = next(file)
    assert line.string == '2' and line.path == '/g' and line.number == 2
    line = next(file)
    assert line.string == 'b' and line.path == '/f' and line.number == 3
    line = next(file)
    assert line.string == '1' and line.path == '/g' and line.number == 1
    line = next(file)
    assert line.string == '2' and line.path == '/g' and line.number == 2
    line = next(file)
    assert line.string == 'c' and line.path == '/f' and line.number == 5


def test_circular_includes(fs):
    fs.create_file('/f', contents='''\
%include /g
''')

    fs.create_file('/g', contents='''\
%include /f
''')

    file = default_specfile('/f')
    with pytest.raises(CircularIncludeException):
        next(file)


def test_relative_paths(fs):
    fs.create_dir('/d')
    fs.create_dir('/e')

    fs.create_file('/d/f', contents='''\
%include ../e/g
''')

    fs.create_file('/e/g', contents='''\
a
''')

    file = default_specfile('/d/f')
    line = next(file)
    assert line.string == 'a'

