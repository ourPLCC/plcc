from pytest import mark, raises, fixture


from . import read_sections, Section, Line, Path, Block, CircularIncludeError


def test_empty(fs):
    fs.create_file('/a', contents='''''')
    assert read_sections('/a') == [Section([])]


def test_one(fs):
    fs.create_file('/a', contents='''one''')
    assert read_sections('/a') == [Section([Line('one', 1, '/a')])]


def test_two_empty(fs):
    fs.create_file('/a', contents='''%''')
    assert read_sections('/a') == [
        Section([]),
        Section([Line('%', 1, '/a')]),
    ]


def test_three_empty(fs):
    fs.create_file('/a', contents='''%\n%''')
    assert read_sections('/a') == [
        Section([]),
        Section([Line('%', 1, '/a')]),
        Section([Line('%', 2, '/a')]),
    ]


def test_more_lines(fs):
    fs.create_file('/a', contents='''\
one
two
% java
three
% python
four
five
''')
    assert read_sections('/a') == [
        Section([
            Line('one', 1, '/a'),
            Line('two', 2, '/a'),
        ]),
        Section([
            Line('% java', 3, '/a'),
            Line('three', 4, '/a'),
        ]),
        Section([
            Line('% python', 5, '/a'),
            Line('four', 6, '/a'),
            Line('five', 7, '/a'),
        ]),
    ]


def test_blocks(fs):
    fs.create_file('/a', contents='''\
%%{
one
two
%%}
''')
    assert read_sections('/a') == [
        Section([
            Block(
                [
                    Line('%%{', 1, '/a'),
                    Line('one', 2, '/a'),
                    Line('two', 3, '/a'),
                    Line('%%}', 4, '/a'),
                ]
            )
        ]),
    ]


def test_include(fs):
    fs.create_file('/a', contents='''\
%include /b
''')
    fs.create_file('/b', contents='''\
one
''')
    assert read_sections('/a') == [
        Section([
            Line('one', 1, '/b'),
        ]),
    ]


def test_relative_include(fs):
    fs.create_file('/f/a', contents='''\
%include ../g/b
''')
    fs.create_file('/g/b', contents='''\
%include h/c
''')
    fs.create_file('/g/h/c', contents='''\
one
''')
    assert read_sections('/f/a') == [
        Section([
            Line('one', 1, '/g/h/c'),
        ]),
    ]


def test_circular_include(fs):
    fs.create_file('/a', contents='''\
%include /b
''')
    fs.create_file('/b', contents='''\
%include /a
''')
    with raises(CircularIncludeError) as info:
        read_sections('/a')
    exception = info.value
    assert exception.line == Line('%include /a', 1, '/b')
