import re

from .bnfrule import BnfRule
from .bnfrule import Tnt
from .bnfspec import BnfSpec


class BnfParserPatterns:
    def __init__(self):
        self.rule = re.compile(r'^(?P<lhs>.*)(?P<op>::=|\*\*=)(?P<rhs>.*)$')
        self.tnt = re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<alt>\w*)|)')
        self.terminal = re.compile(r'^[A-Z_]+$')
        self.separator = re.compile(r'\s*\+')
        self.eolComment = re.compile(r'\s*#.*')


class BnfParser:
    def __init__(self, patterns=None):
        if not patterns:
            patterns = BnfParserPatterns()
        self._patterns = patterns

    def parseBnfSpec(self, lines):
        return BnfSpec(list(self.parseBnfRules(lines)))

    def parseBnfRules(self, lines):
        for line in lines:
            yield self.parseBnfRule(line)

    def parseBnfRule(self, line):
        m = self._patterns.rule.match(line.string)
        if not m:
            raise self.MissingDefinitionOperator()
        lhs, op, rhs = m['lhs'], m['op'], m['rhs']
        nt = self.parseNonterminal(lhs)
        tnts, sep = self.parserRhs(rhs)
        # if op != '**=' and sep:
        #     raise self.StandardRuleCannotHaveSeparator()
        return self.makeBnfRule(line, nt, op, tnts, sep)

    class MissingDefinitionOperator(Exception):
        pass

    class StandardRuleCannotHaveSeparator(Exception):
        pass

    def parseNonterminal(self, lhs):
        tnt = self.parseTnt(MatchScanner(lhs))
        if tnt.isTerminal:
            raise self.InvalidNonterminal()
        return tnt

    def parserRhs(self, rhs):
        s = MatchScanner(rhs)
        tnts = self.parseTnts(s)
        sep = self.parseSeparator(s)
        self.parseEolComment(s)
        if s.hasMore():
            raise self.ExtraContent(s.getRemainder())
        return (tnts, sep)

    def parseTnts(self, scanner):
        tnts = []
        try:
            while True:
                tnts.append(self.parseTnt(scanner))
        except self.InvalidTnt:
            pass
        return tnts

    def makeBnfRule(self, line, nt, op, tnts, sep):
        return BnfRule(line=line, lhs=nt, isRepeating=op=='**=', tnts=tnts, sep=sep)

    class ExtraContent(Exception):
        pass

    class InvalidNonterminal(Exception):
        pass

    def parseTnt(self, matchScanner):
        self._scanner = matchScanner
        m = self._scanner.match(self._patterns.tnt)
        if not m:
            raise self.InvalidTnt()
        name = m['name']
        isCapture = bool(m['angle'])
        isTerminal = not isCapture or bool(self._patterns.terminal.match(name))
        alt = '' if not isCapture else m['alt']
        return Tnt(isTerminal=isTerminal, name=name, alt=alt, isCapture=isCapture)

    class InvalidTnt(Exception):
        pass

    class InvalidTerminal(Exception):
        pass

    def parseSeparator(self, matchScanner):
        m = matchScanner.match(self._patterns.separator)
        if m:
            tnt = BnfParser().parseTnt(matchScanner)
            return tnt
        return None

    class SeparatorMustBeTerminal(Exception):
        pass

    class SeparatorMustNotBeInAngles(Exception):
        pass

    class InvalidSeparator(Exception):
        pass

    def parseEolComment(self, matchScanner):
        m = matchScanner.match(self._patterns.eolComment)
        return m


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
