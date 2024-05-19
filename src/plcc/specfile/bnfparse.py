from __future__ import annotations
import functools
import re
from dataclasses import dataclass
from typing import List


class BnfParser:
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
        return NonterminalParser().parse(lhs)

    def _parserRhs(self, rhs):
        return RhsParser().parse(rhs)

    def _makeBnfRule(self, nt, op, tnts, sep):
        if op == '**=':
            return self._makeRepeatingRule(nt, tnts, sep)
        else:
            return self._makeStandardRule(nt, tnts)
        return BnfRule(nt, op, tnts, sep)

    def _makeRepeatingRule(self, nt, tnts, sep):
        return RepeatingRule(nt, tnts, sep)

    def _makeStandardRule(self, nt, tnts):
        return StandardRule(nt, tnts)


@dataclass
class StandardRule:
    lhs: Nonterminal
    tnts: List[Terminal | Nonterminal | CaptureTerminal]


@dataclass
class RepeatingRule:
    lhs: Nonterminal
    tnts: List[Terminal | Nonterminal | CaptureTerminal]
    sep: Terminal


class NonterminalParser:
    def parse(self, string):
        p = TntParser()
        tnt, string = p.parse(string)
        if isinstance(tnt, Nonterminal):
            return tnt, string
        raise self.InvalidNonterminalName(tnt.name)

    class InvalidNonterminalName(Exception):
        pass


class TntParser:
    ANGLES=re.compile(r'\s*<\s*(\w*)\s*>')
    ALT=re.compile(r'\s*:?\s*(\w*)')
    def parse(self, string):
        m = self.ANGLES.match(string)
        if not m:
            raise self.MissingAngles(string)
        name = m[1]
        n = len(m[0])
        m = self.ALT.match(string[n:])
        alt = m[1]
        n += len(m[0])
        return (self._makeTnt(name, alt), string[n:])

    class MissingAngles(Exception):
        pass

    def _makeTnt(self, name, alt):
        if self._isValidTerminalName(name):
            return self._makeCaptureTerminal(name, alt)
        else:
            return self._makeNonterminal(name, alt)

    def _isValidTerminalName(self, name):
        try:
            TerminalParser().parse(name)
            return True
        except TerminalParser.InvalidTerminalName:
            return False

    def _makeNonterminal(self, name, alt):
        return Nonterminal(name, alt)

    def _makeCaptureTerminal(self, name, alt):
        return CaptureTerminal(name, alt)


@dataclass(frozen=True)
class Nonterminal:
    name: str
    alt: str


@dataclass(frozen=True)
class CaptureTerminal:
    name: str
    alt: str


@dataclass(frozen=True)
class Terminal:
    name: str


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
                except TntParser.MissingAngles:
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
        print(f'TerminalParser: {string}')
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

