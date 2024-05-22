from dataclasses import dataclass
import re


from plcc.specfile.line import Line
from .lexrule import LexRule


class LexParserPatterns:
    def __init__(self):
        self.rule = re.compile(r'^\s*(?:(?P<type>skip|token)\s+)?(?P<name>[A-Z_]+)\s+(?P<quote>[\'"])(?P<pattern>[^(?P=quote)]*)(?P=quote)(?P<end>.*)$')


class LexParser:
    def __init__(self, lexParserPatterns=None):
        if not lexParserPatterns:
            lexParserPatterns = LexParserPatterns()
        self._patterns = lexParserPatterns

    def parse(self, lines):
        for line in lines:
            s = line.string.strip()
            m = self._patterns.rule.match(line.string)
            if not m:
                raise self.InvalidLexRule(line)
            d = m.groupdict()
            if not d['type']:
                d['type'] = 'token'
            d['line'] = line
            yield LexRule(**d)

    class InvalidLexRule(Exception):
        pass
