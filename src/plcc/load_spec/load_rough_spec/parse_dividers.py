from dataclasses import dataclass
import re


from .parse_lines import Line


@dataclass
class Divider:
    line: Line


def parse_dividers(lines, pattern=re.compile(r'^%(?:\s.*)?$'), Divider=Divider):
    if lines is None:
        return
    for line in lines:
        if isinstance(line, Line) and pattern.match(line.string):
            yield Divider(line)
        else:
            yield line
