from . import make_blocks, Line, Block
from ..make_lines import make_lines


def test_integration():
    assert make_blocks(make_lines('''
before one
%%%
one
%%% # comments allowed
before two
%%{
%%% # part of block, so doesn't start a new block
%%{ # ditto
two
%%}
    ''')) == [
        Line('', 1, file=None),
        Line('before one', 2, None),
        Block(
            open=Line('%%%', 3, None),
            lines=[
                Line('one', 4, None),
            ],
            close=Line('%%% # comments allowed', 5, None)
        ),
        Line('before two', 6, None),
        Block(
            open=Line('%%{', 7, None),
            lines=[
                Line('%%% # part of block, so doesn\'t start a new block', 8, None),
                Line('%%{ # ditto', 9, None),
                Line('two', 10, None),
            ],
            close=Line('%%}', 11, None)
        ),
        Line('    ', 12, None)
    ]
