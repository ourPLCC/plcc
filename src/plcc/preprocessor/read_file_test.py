from pytest import raises, mark, fixture


from .read_file import read_file


def test_None_errors():
    with raises(TypeError):
        read_file(None)


def test_nonexistent_errors(fs):
    with raises(FileNotFoundError):
        read_file('does_not_exist')


def test_without_read_permissions_errors(fs):
    fs.create_file('/no_read')
    fs.chmod('/no_read', 0o000)
    with raises(PermissionError):
        read_file('/no_read')


def test_empty_returns_empty(fs):
    fs.create_file('/empty')
    assert read_file('/empty') == ''


def test_returns_entire_file_as_string(fs):
    contents='''\
hi there
    one big string
        coming up!
'''

    fs.create_file('/f', contents=contents)
    assert read_file('/f') == contents
