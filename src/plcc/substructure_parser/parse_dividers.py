from dataclasses import dataclass
import re


from .parse_lines import Line


@dataclass
class Divider:
    line: Line


def parse_dividers(lines):
    if lines is None:
        return
    for line in lines:
        if isinstance(line, Line) and re.match(r'^%(?:[^%].*)?$', line.string):
            yield Divider(line)
        else:
            yield line
