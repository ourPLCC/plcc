from __future__ import annotations
import functools
import re
from dataclasses import dataclass
from typing import List


class BnfParser:
    def parse(self, lines):
        return lines


class BnfRuleParser:
    RULE=re.compile(r'^(.*)(::=|\*\*=)(.*)$')
    def parse(self, string):
        m = self.RULE.match(string)
        if not m:
            raise self.MissingDefinition()
        lhs, op, rhs = m[1], m[2], m[3]
        nt = self._parseNonterminal(lhs)
        tnts, sep = self._parserRhs(rhs)
        if op != '**=' and sep:
            raise self.IllegalSeparator('Non repeating rules (::=) cannot have a separator clause (+).')
        return self._makeBnfRule(nt, op, tnts, sep)

    class MissingDefinition(Exception):
        pass

    class IllegalSeparator(Exception):
        pass

    def _parseNonterminal(self, lhs):
        nt, remaining = NonterminalParser().parse(lhs)
        return nt

    def _parserRhs(self, rhs):
        return RhsParser().parse(rhs)

    def _makeBnfRule(self, nt, op, tnts, sep):
        return self._makeBnfRule(nt, op, tnts, sep)

    def _makeBnfRule(self, nt, op, tnts, sep):
        return BnfRule(nt, op, tnts, sep)


@dataclass
class BnfRule:
    lhs: Nonterminal
    op: str
    tnts: List[Terminal | Nonterminal | CaptureTerminal]
    sep: Terminal = None


@dataclass
class RepeatingRule:
    lhs: Nonterminal
    tnts: List[Terminal | Nonterminal | CaptureTerminal]
    sep: Terminal


class NonterminalParser:
    def parse(self, string):
        p = TntParser()
        tnt, string = p.parse(string)
        if tnt.type == 'nonterminal':
            return tnt, string
        raise self.InvalidNonterminalName(tnt.name)

    class InvalidNonterminalName(Exception):
        pass


class TntParser:
    PATTERN=re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<alt>\w*)|)')
    TERMINAL=re.compile(r'^[A-Z_]+$')

    def __init__(self):
        self._scanner = None

    def parse(self, string):
        self._scanner = MatchScanner(string)
        m = self._scanner.match(self.PATTERN)
        if not m:
            raise self.InvalidTnt(string)
        name = m['name']
        type = 'terminal' if self.TERMINAL.match(name) else 'nonterminal'
        capture = bool(m['angle'])
        alt = '' if not capture else m['alt']
        if not capture and type == 'nonterminal':
            raise self.InvalidTerminal(string)
        return Tnt(type,name,alt,capture), self._scanner.getRemainder()

    class InvalidTnt(Exception):
        pass

    class InvalidTerminal(Exception):
        pass

class MatchScanner:
    def __init__(self, string):
        self._string = string
        self._position = 0

    def match(self, pattern):
        m = pattern.match(self._string, self._position)
        if m:
            self._position += len(m[0])
        return m

    def getRemainder(self):
        return self._string[self._position:]


@dataclass(frozen=True)
class Tnt:
    type: str
    name: str
    alt: str
    capture: bool


class RhsParser:
    def parse(self, string):
        tnts, string = self._parseTnts(string)
        sep, string = self._parseSeparator(string)
        _, string = self._parseEolComment(string)
        if string:
            raise self.Unrecognized(string)
        return tnts, sep

    class Unrecognized(Exception):
        pass

    def _parseTnts(self, string):
        tnts = []
        try:
            while True:
                try:
                    tnt, string = self._parseTnt(string)
                    tnts.append(tnt)
                except TntParser.InvalidTnt:
                    term, string = self._parseTerminal(string)
                    tnts.append(term)
        except TerminalParser.InvalidTerminalName:
            pass
        return (tnts, string)

    def _parseTnt(self, string):
        return TntParser().parse(string)

    def _parseTerminal(self, string):
        return TerminalParser().parse(string)

    def _parseSeparator(self, string):
        return SeparatorParser().parse(string)

    def _parseEolComment(self, string):
        return EolCommentParser().parse(string)


class TerminalParser:
    TERMINAL=re.compile(r'\s*([A-Z_]+)')
    def parse(self, string):
        m = self.TERMINAL.match(string)
        if m:
            return (m[1], string[len(m[0]):])
        raise self.InvalidTerminalName(string)

    class InvalidTerminalName(Exception):
        pass


class SeparatorParser:
    SEPARATOR=re.compile(r'\s*\+(' + TerminalParser.TERMINAL.pattern + ')')
    def parse(self, string):
        m = self.SEPARATOR.match(string)
        if m:
            return (m[1], string[len(m[0]):])
        return ('', string)


class EolCommentParser:
    EOL_COMMENT=re.compile(r'\s*#.*')
    def parse(self, string):
        m = self.EOL_COMMENT.match(string)
        if m:
            return (m[0], string[len(m[0]):])
        return ('', string)

