from dataclasses import dataclass
import re


from .lines import Line


@dataclass(frozen=True)
class Include():
    file: str
    line: Line


def parse_includes(
        lines,
        pattern=re.compile(r'^%include\s+(?P<file>[^\0]+)$'),
        Include=Include
        ):
    if lines is None:
        return
    for line in lines:
        try:
            m = re.match(pattern, line.string)
            if m:
                yield Include(file=m['file'], line=line)
            else:
                yield line
        except AttributeError: # line is not a Line
            yield line
