from pytest import raises, mark, fixture


from . import preprocess_file, Line, Block


def test_preprocessor(fs):
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

    assert list(preprocess_file('/a')) == [
        Line('one', 1, '/a'),
        Line('two', 1, '/f/b'),
        Block([
            Line('%%%', 1, '/g/c'),
            Line('three', 2, '/g/c'),
            Line('%%%', 3, '/g/c')
        ])
    ]
