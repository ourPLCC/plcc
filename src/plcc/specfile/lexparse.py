from dataclasses import dataclass
import re


from ..specfile.line import Line


def parse(lines):
    rules = []
    for line in lines:
        s = line.string.strip()
        if not s:
            continue
        if s[0] == '#':
            continue
        m = re.match(r'^\s*(?:(?P<type>skip|token)\s+)?(?P<name>[A-Z_]+)\s+(?P<quote>[\'"])(?P<pattern>[^(?P=quote)]*)(?P=quote)(?P<end>.*)$', line.string)
        d = m.groupdict()
        if not d['type']:
            d['type'] = 'token'
        d['line'] = line
        rules.append(LexRule(**d))
    return rules


@dataclass(frozen=True)
class LexRule:
    type: str
    name: str
    pattern: str
    quote: str
    end: str
    line: Line
