import pytest


from plcc.spec import parse
from plcc.specfile import specfile


def test_parse_three_empty_sections(fs):
    fs.create_file('/f', contents='''\
%
%
''')
    spec = parse(specfile('/f'))
