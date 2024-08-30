from __future__ import annotations
from abc import ABC, abstractmethod
import re


from ...read_sections import Line


def parse(builder: Builder, lines: str|[str]|[Line]) -> None:
    rule_pat = re.compile(r'^\s*(?:(?P<type>skip|token)\s+)?(?P<name>[A-Z_]+)\s+(?P<quote>[\'"])(?P<pattern>[^(?P=quote)]*)(?P=quote)(?:\s*(?:#.*)?)$')
    blank_pat = re.compile(r'^\s*$')
    comment_pat = re.compile(r'^\s*#.*$')
    builder.begin()
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


class ParseError(Exception):
    def __init__(self, line):
        self.line = line


class Builder(ABC):
    @abstractmethod
    def begin(self) -> None:
        '''Parsing has begun.'''

    @abstractmethod
    def addTokenRule(self, name: str, pattern: str, line: Line) -> None:
        '''Implicit or explicit token rule encountered.'''

    @abstractmethod
    def addSkipRule(self, name: str, pattern: str, line: Line) -> None:
        '''Skip rule encountered.'''

    @abstractmethod
    def end(self) -> None:
        '''Parsing is done.'''
