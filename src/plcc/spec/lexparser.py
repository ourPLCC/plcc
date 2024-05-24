from dataclasses import dataclass
import re


from plcc.spec.line import Line
from .lexrule import LexRule


class LexParserPatterns:
    def __init__(self):
        self.rule = re.compile(r'^\s*(?:(?P<isToken>skip|token)\s+)?(?P<name>[A-Z_]+)\s+(?P<quote>[\'"])(?P<pattern>[^(?P=quote)]*)(?P=quote)(?P<remainder>.*)$')


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
            d['isToken'] = not d['isToken'] or d['isToken'] == 'token'
            d['line'] = line
            del d['quote']
            yield LexRule(**d)

    class InvalidLexRule(Exception):
        pass
