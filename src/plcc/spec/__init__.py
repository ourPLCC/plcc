from __future__ import annotations
from typing import Iterable
from gettext import gettext as _
import re
from dataclasses import dataclass

from ..specfile.line import Line


def parse(lines):
    p = Parser()
    p.parse(lines)
    return p.getSpec()


class Parser():
    def __init__(self):
        self._spec = Spec()

    def parse(self, lines):
        if lines is None:
            raise TypeError(_('`lines` must be an iterable of `Line`.'))
        self._parseLexicalSpecification(lines)

    def _parseLexicalSpecification(self, lines):
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
                self._spec.addLexRule(LexRule(**d))


    def getSpec(self) -> Spec:
        return self._spec


class Spec():
    def __init__(self):
        self._lexRules = []

    def addLexRule(self, rule):
        self._lexRules.append(rule)

    def getLexRules(self):
        return self._lexRules


@dataclass(frozen=True)
class LexRule:
    type: str
    name: str
    pattern: str
    quote: str
    end: str
    line: Line
