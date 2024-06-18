import re


from .builder import LexicalTreeBuilder
from ...read_sections import Line


class ParseError(Exception):
    def __init__(self, line):
        self.line = line


def parse(lines):
    builder = LexicalTreeBuilder()
    _parse_lines(builder, lines)
    tree = builder.result
    return tree


def toLines(string):
    return string.splitlines()

def _parse_lines(builder, lines):
    rule_pat = re.compile(r'^\s*(?:(?P<type>skip|token)\s+)?(?P<name>[A-Z_]+)\s+(?P<quote>[\'"])(?P<pattern>[^(?P=quote)]*)(?P=quote)(?:\s*(?:#.*)?)$')
    blank_pat = re.compile(r'^\s*$')
    comment_pat = re.compile(r'^\s*#.*$')
    builder.begin()
    if lines is not None:
        lines = Line.asLines(lines)
        for line in lines:
            m = rule_pat.match(line.string)
            if m:
                if m['type'] is None or m['type'] == 'token':
                    builder.addTokenRule(m['name'], m['pattern'], line)
                else:
                    builder.addSkipRule(m['name'], m['pattern'], line)
                continue
            m = blank_pat.match(line.string)
            if m:
                continue
            m = comment_pat.match(line.string)
            if m:
                continue
            raise ParseError(line)
    builder.end()
