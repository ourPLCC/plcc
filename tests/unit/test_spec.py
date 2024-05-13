import pytest


from plcc.spec import Spec
from plcc.specfiles import default_specfile



def test_parse_three_empty_sections(fs):
    fs.create_file('/f', contents='''\
%
%
''')
    s = Spec()
    s.parse(default_specfile('/f'))
    assert s.getSectionCount() == 3
