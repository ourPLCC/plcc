from pytest import raises, mark, fixture


from .preparse_file import preparse_file, Line, Block


def test_preparse_file(fs):
    fs.create_file('/a', contents='''\
one
%include f/b
''')
    fs.create_file('/f/b', contents='''\
two
%include ../g/c
''')
    fs.create_file('/g/c', contents='''\
%%%
three
%%%
''')

    assert list(preparse_file('/a')) == [
        Line('one', 1, '/a'),
        Line('two', 1, '/f/b'),
        Block([
            Line('%%%', 1, '/g/c'),
            Line('three', 2, '/g/c'),
            Line('%%%', 3, '/g/c')
        ])
    ]
