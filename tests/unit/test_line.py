import pytest
import os


from plcc.specfile.line import readLinesFromSpecFile, CircularIncludeException


@pytest.mark.focus
def test_lines_contain_contents_without_eol(fs):
    fs.create_file('/f', contents=
        'one\n'
        'two\n'
    )
    lines = readLinesFromSpecFile('/f')
    line = next(lines)
    assert line.string == 'one'
    line = next(lines)
    assert line.string == 'two'


@pytest.mark.focus
def test_lines_are_numbered_from_1(fs):
    fs.create_file('/f', contents=
        'one\n'
        'two\n'
    )
    lines = readLinesFromSpecFile('/f')
    line = next(lines)
    assert line.number == 1
    line = next(lines)
    assert line.number == 2


@pytest.mark.focus
def test_lines_contain_absolute_path(fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        'two\n'
    )
    os.chdir('/a')
    lines = readLinesFromSpecFile('b/f')
    line = next(lines)
    assert line.path == '/a/b/f'
    line = next(lines)
    assert line.path == '/a/b/f'


@pytest.mark.focus
def test_lines_skip_blank_lines(fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '\n'
        'three\n'
    )
    os.chdir('/a')
    lines = readLinesFromSpecFile('b/f')
    line = next(lines)
    assert line.string == 'one' and line.number == 1
    line = next(lines)
    assert line.string == 'three' and line.number == 3


@pytest.mark.focus
def test_lines_skip_comment_lines(fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '   #this is a comment line\n'
        'three\n'
    )
    os.chdir('/a')
    lines = readLinesFromSpecFile('b/f')
    line = next(lines)
    assert line.string == 'one' and line.number == 1
    line = next(lines)
    assert line.string == 'three' and line.number == 3


@pytest.mark.focus
def test_blocks_are_marked(fs):
    fs.create_file('/f', contents=
        'one\n'
        '%%%\n'
        'a\n'
        'b\n'
        '%%%\n'
        'two\n'
    )
    lines = readLinesFromSpecFile('/f')
    line = next(lines)
    assert not line.isInBlock and line.string == 'one'
    line = next(lines)
    assert not line.isInBlock and line.string == '%%%'
    line = next(lines)
    assert line.isInBlock and line.string == 'a'
    line = next(lines)
    assert line.isInBlock and line.string == 'b'
    line = next(lines)
    assert not line.isInBlock and line.string == '%%%'
    line = next(lines)
    assert not line.isInBlock and line.string == 'two'


@pytest.mark.focus
def test_blanks_not_skipped_in_blocks(fs):
    fs.create_file('/f', contents=
        'one\n'
        '%%%\n'
        'a\n'
        '\n'
        'b\n'
        '%%%\n'
        'two\n'
    )
    lines = readLinesFromSpecFile('/f')
    line = next(lines)
    assert not line.isInBlock
    line = next(lines)
    assert not line.isInBlock
    line = next(lines)
    assert line.isInBlock
    line = next(lines)
    assert line.isInBlock and line.string == ''
    line = next(lines)
    assert line.isInBlock
    line = next(lines)
    assert not line.isInBlock
    line = next(lines)
    assert not line.isInBlock


@pytest.mark.focus
def test_comments_not_skipped_in_blocks(fs):
    fs.create_file('/f', contents=
        'one\n'
        '%%%\n'
        'a\n'
        '    # comment\n'
        'b\n'
        '%%%\n'
        'two\n'
    )
    lines = readLinesFromSpecFile('/f')
    line = next(lines)
    assert not line.isInBlock
    line = next(lines)
    assert not line.isInBlock
    line = next(lines)
    assert line.isInBlock
    line = next(lines)
    assert line.isInBlock and line.string == '    # comment'
    line = next(lines)
    assert line.isInBlock
    line = next(lines)
    assert not line.isInBlock
    line = next(lines)
    assert not line.isInBlock


@pytest.mark.focus
def test_includes(fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '%include ../c/g\n'
        'three\n'
    )
    fs.create_dir('/a/c')
    fs.create_file('/a/c/g', contents=
        'alpha\n'
        'bravo'
    )
    lines = readLinesFromSpecFile('/a/b/f')
    line = next(lines)
    assert line.string == 'one' and line.path == '/a/b/f' and line.number == 1
    line = next(lines)
    assert line.string == 'alpha' and line.path == '/a/c/g' and line.number == 1
    line = next(lines)
    assert line.string == 'bravo' and line.path == '/a/c/g' and line.number == 2
    line = next(lines)
    assert line.string == 'three' and line.path == '/a/b/f' and line.number == 3


@pytest.mark.focus
def test_circular_includes_detected(fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '%include ../c/g\n'
        'three\n'
    )

    fs.create_dir('/a/c')
    fs.create_file('/a/c/g', contents=
        'alpha\n'
        '%include ../b/f\n'
        'bravo\n'
    )

    lines = readLinesFromSpecFile('/a/b/f')

    line = next(lines)
    line = next(lines)
    with pytest.raises(CircularIncludeException) as info:
        next(lines)
    e = info.value
    assert e.line.path == '/a/c/g' and e.line.number == 2 and e.line.string == '%include ../b/f'


@pytest.mark.focus
def test_includes_ignored_in_blocks(fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '%%%\n'
        '%include ../c/g\n'
        '%%%\n'
        'three\n'
    )

    fs.create_dir('/a/c')
    fs.create_file('/a/c/g', contents=
        'alpha\n'
        '%include ../b/f\n'
        'bravo\n'
    )

    lines = readLinesFromSpecFile('/a/b/f')

    line = next(lines)
    assert line.string == 'one'
    line = next(lines)
    assert line.string == '%%%'
    line = next(lines)
    assert line.string == '%include ../c/g'
    line = next(lines)
    assert line.string == '%%%'
    line = next(lines)
    assert line.string == 'three'
