from dataclasses import dataclass
import re


from plcc.spec.line import Line
from .lexrule import LexRule


class LexParser:
    def __init__(self, lexParserPatterns=None):
        self._rulePattern = re.compile(r'^\s*(?:(?P<isToken>skip|token)\s+)?(?P<name>[A-Z_]+)\s+(?P<quote>[\'"])(?P<pattern>[^(?P=quote)]*)(?P=quote)(?P<remainder>.*)$')

    def parse(self, lines):
        for line in lines:
            s = line.string.strip()
            m = self._rulePattern.match(line.string)
            if not m:
                raise self.InvalidLexRule(line)
            d = m.groupdict()
            d['isToken'] = not d['isToken'] or d['isToken'] == 'token'
            d['line'] = line
            del d['quote']
            yield LexRule(**d)

    class InvalidLexRule(Exception):
        pass
