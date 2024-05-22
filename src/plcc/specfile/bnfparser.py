from __future__ import annotations
import functools
import re
from dataclasses import dataclass
from typing import List


from .bnfrule import BnfRule, Tnt


class BnfParser:
    def parse(self, lines):
        for line in lines:
            yield self._parseBnfRule(line)

    def _parseBnfRule(self, line):
        return BnfRuleParser().parse(line.string)


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
        return NonterminalParser().parse(MatchScanner(lhs))

    def _parserRhs(self, rhs):
        s = MatchScanner(rhs)
        tnts = self._parseTnts(s)
        sep = self._parseSeparator(s)
        self._parseEolComment(s)
        if s.hasMore():
            raise self.Unrecognized(s.getRemainder())
        return (tnts, sep)

    def _parseTnts(self, scanner):
        tnts = []
        try:
            while True:
                tnts.append(TntParser().parse(scanner))
        except TntParser.InvalidTnt:
            pass
        return tnts

    def _parseSeparator(self, scanner):
        return SeparatorParser().parse(scanner)

    def _parseEolComment(self, scanner):
        return EolCommentParser().parse(scanner)

    def _makeBnfRule(self, nt, op, tnts, sep):
        return self._makeBnfRule(nt, op, tnts, sep)

    def _makeBnfRule(self, nt, op, tnts, sep):
        return BnfRule(nt, op, tnts, sep)

    class Unrecognized(Exception):
        pass


class NonterminalParser:
    def parse(self, matchScanner):
        p = TntParser()
        tnt = p.parse(matchScanner)
        if tnt.type == 'nonterminal':
            return tnt
        raise self.InvalidNonterminal()

    class InvalidNonterminal(Exception):
        pass


class TntParser:
    PATTERN=re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<alt>\w*)|)')
    TERMINAL=re.compile(r'^[A-Z_]+$')

    def __init__(self):
        self._scanner = None

    def parse(self, matchScanner):
        self._scanner = matchScanner
        m = self._scanner.match(self.PATTERN)
        if not m:
            raise self.InvalidTnt()
        name = m['name']
        type = 'terminal' if self.TERMINAL.match(name) else 'nonterminal'
        capture = bool(m['angle'])
        alt = '' if not capture else m['alt']
        if not capture and type == 'nonterminal':
            raise self.InvalidTerminal()
        return Tnt(type,name,alt,capture)

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

    def hasMore(self):
        return self._position < len(self._string)


class SeparatorParser:
    SEPARATOR=re.compile(r'\s*\+')
    def parse(self, matchScanner):
        m = matchScanner.match(self.SEPARATOR)
        if m:
            tnt = TntParser().parse(matchScanner)
            if tnt.type != 'terminal':
                raise self.SeparatorMustBeTerminal()
            if tnt.capture:
                raise self.SeparatorMustNotBeInAngles()
            return tnt
        return None

    class SeparatorMustBeTerminal(Exception):
        pass

    class SeparatorMustNotBeInAngles(Exception):
        pass

    class InvalidSeparator(Exception):
        pass


class EolCommentParser:
    EOL_COMMENT=re.compile(r'\s*#.*')
    def parse(self, matchScanner):
        m = matchScanner.match(self.EOL_COMMENT)
        return m

