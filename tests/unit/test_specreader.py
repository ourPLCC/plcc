import pytest
import os


from plcc.spec.reader import SpecReader


@pytest.fixture
def reader():
    return SpecReader()


def test_lines_contain_contents_without_eol(reader, fs):
    fs.create_file('/f', contents=
        'one\n'
        'two\n'
    )
    lines = reader.readLinesFromSpecFile('/f')
    line = next(lines)
    assert line.string == 'one'
    line = next(lines)
    assert line.string == 'two'


def test_lines_are_numbered_from_1(reader, fs):
    fs.create_file('/f', contents=
        'one\n'
        'two\n'
    )
    lines = reader.readLinesFromSpecFile('/f')
    line = next(lines)
    assert line.number == 1
    line = next(lines)
    assert line.number == 2


def test_lines_contain_absolute_path(reader, fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        'two\n'
    )
    os.chdir('/a')
    lines = reader.readLinesFromSpecFile('b/f')
    line = next(lines)
    assert line.path == '/a/b/f'
    line = next(lines)
    assert line.path == '/a/b/f'


def test_lines_skip_blank_lines(reader, fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '\n'
        'three\n'
    )
    os.chdir('/a')
    lines = reader.readLinesFromSpecFile('b/f')
    line = next(lines)
    assert line.string == 'one' and line.number == 1
    line = next(lines)
    assert line.string == 'three' and line.number == 3


def test_lines_skip_comment_lines(reader, fs):
    fs.create_dir('/a/b')
    fs.create_file('/a/b/f', contents=
        'one\n'
        '   #this is a comment line\n'
        'three\n'
    )
    os.chdir('/a')
    lines = reader.readLinesFromSpecFile('b/f')
    line = next(lines)
    assert line.string == 'one' and line.number == 1
    line = next(lines)
    assert line.string == 'three' and line.number == 3


def test_blocks_are_marked(reader, fs):
    fs.create_file('/f', contents=
        'one\n'
        '%%%\n'
        'a\n'
        'b\n'
        '%%%\n'
        'two\n'
    )
    lines = reader.readLinesFromSpecFile('/f')
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


def test_blanks_not_skipped_in_blocks(reader, fs):
    fs.create_file('/f', contents=
        'one\n'
        '%%%\n'
        'a\n'
        '\n'
        'b\n'
        '%%%\n'
        'two\n'
    )
    lines = reader.readLinesFromSpecFile('/f')
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


def test_comments_not_skipped_in_blocks(reader, fs):
    fs.create_file('/f', contents=
        'one\n'
        '%%%\n'
        'a\n'
        '    # comment\n'
        'b\n'
        '%%%\n'
        'two\n'
    )
    lines = reader.readLinesFromSpecFile('/f')
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


def test_includes(reader, fs):
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
    lines = reader.readLinesFromSpecFile('/a/b/f')
    line = next(lines)
    assert line.string == 'one' and line.path == '/a/b/f' and line.number == 1
    line = next(lines)
    assert line.string == 'alpha' and line.path == '/a/c/g' and line.number == 1
    line = next(lines)
    assert line.string == 'bravo' and line.path == '/a/c/g' and line.number == 2
    line = next(lines)
    assert line.string == 'three' and line.path == '/a/b/f' and line.number == 3


def test_circular_includes_detected(reader, fs):
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

    lines = reader.readLinesFromSpecFile('/a/b/f')

    line = next(lines)
    line = next(lines)
    with pytest.raises(SpecReader.CircularIncludeException) as info:
        next(lines)
    e = info.value
    assert e.line.path == '/a/c/g' and e.line.number == 2 and e.line.string == '%include ../b/f'


def test_includes_ignored_in_blocks(reader, fs):
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

    lines = reader.readLinesFromSpecFile('/a/b/f')

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


def test_can_read_lines_into_sections(reader, fs):
    fs.create_file('/f', contents=
        'one\n'
        '%\n'       # Section separator
        'two\n'
        '%\n'       # Another
        '%\n'       # Another
    )
    sections = reader.readSectionsFromSpecFile('/f')

    # There are 4 sections.
    assert len(sections) == 4

    # Each section contains the lines that compose it.
    lines = sections[0]
    assert lines[0].string == 'one'

    # The last two are empty.
    assert len(sections[2]) == 0
    assert len(sections[3]) == 0
