from .parse_lines import parse_lines
from .parse_blocks import parse_blocks
from .parse_dividers import parse_dividers
from .parse_includes import parse_includes


def parse_substructure(string, file=None):
    return parse_dividers(parse_includes(parse_blocks(parse_lines(
        string,
        file=file
    ))))
