import re

from ..spec.bnfrule import BnfRule
from ..spec.bnfrule import Symbol
from ..spec.bnfspec import BnfSpec


class BnfParser:
    def __init__(self):
        self._rulePattern = re.compile(r'^(?P<lhs>.*)(?P<op>::=|\*\*=)(?P<rhs>.*)$')
        self._symbolPattern = re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<alt>\w*)|)')
        self._terminalPattern = re.compile(r'^[A-Z_]+$')
        self._startSeparatorPattern = re.compile(r'\s*\+')
        self._eolCommentPattern = re.compile(r'\s*#.*')

    def parseBnfSpec(self, lines):
        return BnfSpec(list(self.parseBnfRules(lines)))

    def parseBnfRules(self, lines):
        for line in lines:
            yield self.parseBnfRule(line)

    def parseBnfRule(self, line):
        lhs, rhs, op = self.splitRule(line)
        leftHandSymbol = self.parseLhs(lhs)
        rightHandSymbols, separator = self.parserRhs(rhs)
        return BnfRule(
            line=line,
            leftHandSymbol=leftHandSymbol,
            isRepeating=self._isRepeatingRule(op),
            rightHandSymbols=rightHandSymbols,
            separator=separator
        )

    def splitRule(self, line):
        m = self._rulePattern.match(line.string)
        if not m:
            raise self._InvalidBnfRule()
        lhs, op, rhs = m['lhs'], m['op'], m['rhs']
        return lhs, rhs, op

    class _InvalidBnfRule(Exception):
        pass

    def parseLhs(self, lhs):
        return LeftHandSideParser(self._symbolPattern, self._terminalPattern).parse(lhs)

    def parserRhs(self, rhs):
        return RightHandSideParser(
            self._symbolPattern,
            self._terminalPattern,
            self._startSeparatorPattern,
            self._eolCommentPattern).parse(rhs)

    def _isRepeatingRule(self, operator):
        return operator=='**='

    def parseSymbol(self, matchScanner):
        return SymbolParser(self._symbolPattern, self._terminalPattern).parse(matchScanner)


class SymbolParser:
    def __init__(self, symbolPattern, terminalPattern):
        self._symbolPattern = symbolPattern
        self._terminalPattern = terminalPattern

    def parse(self, string):
        m = self._symbolPattern.match(string)
        if not m:
            raise self._InvalidSymbol()
        name = m['name']
        isCapture = bool(m['angle'])
        isTerminal = not isCapture or bool(self._terminalPattern.match(name))
        alt = '' if not isCapture else m['alt']
        symbol = Symbol(isTerminal=isTerminal, name=name, alt=alt, isCapture=isCapture)
        remainder = string[len(m[0]):]
        return (symbol, remainder)

    class _InvalidSymbol(Exception):
        pass


class LeftHandSideParser:
    def __init__(self, symbolPattern, terminalPattern):
        self._symbolPattern = symbolPattern
        self._terminalPattern = terminalPattern

    def parse(self, string):
        symbol, remainder = self.parseSymbol(string)
        if symbol.isTerminal:
            raise self._InvalidLeftHandSide()
        return symbol

    def parseSymbol(self, string):
        return SymbolParser(self._symbolPattern, self._terminalPattern).parse(string)

    class _InvalidLeftHandSide(Exception):
        pass


class RightHandSideParser:
    def __init__(self, symbolPattern, terminalPattern, separatorPattern, eolCommentPattern):
        self._symbolPattern = symbolPattern
        self._terminalPattern = terminalPattern
        self._separatorPattern = separatorPattern
        self._eolCommentPattern = eolCommentPattern

    def parse(self, string):
        unmatched = string
        symbols, unmatched = self.parseRightHandSymbols(unmatched)
        sep, unmatched = self.parseSeparator(unmatched)
        unmatched = self.parseEolComment(unmatched)
        if unmatched:
            raise self._ExtraContent(unmatched)
        return (symbols, sep)

    class _ExtraContent(Exception):
        pass

    def parseRightHandSymbols(self, string):
        unmatched = string
        symbols = []
        try:
            while unmatched:
                sym, unmatched = self.parseSymbol(unmatched)
                symbols.append(sym)
        except SymbolParser._InvalidSymbol:
            pass
        return symbols, unmatched

    def parseSeparator(self, string):
        unmatched = string
        m = self._separatorPattern.match(unmatched)
        if not m:
            return None, unmatched
        else:
            unmatched = unmatched[len(m[0]):]
            return self.parseSymbol(unmatched)

    def parseSymbol(self, string):
        return SymbolParser(self._symbolPattern, self._terminalPattern).parse(string)

    def parseEolComment(self, string):
        m = self._eolCommentPattern.match(string)
        if not m:
            return string
        else:
            return string[len(m[0]):]


InvalidBnfRule = BnfParser._InvalidBnfRule
InvalidLeftHandSide = LeftHandSideParser._InvalidLeftHandSide
InvalidSymbol = SymbolParser._InvalidSymbol
ExtraContent = RightHandSideParser._ExtraContent
