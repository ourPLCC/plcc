import re

from .bnfrule import BnfRule
from .bnfrule import Symbol
from .bnfspec import BnfSpec


class BnfParser:
    def __init__(self):
        self._rulePattern = re.compile(r'^(?P<lhs>.*)(?P<op>::=|\*\*=)(?P<rhs>.*)$')
        self._symbolPattern = re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<alt>\w*)|)')
        self._terminalPattern = re.compile(r'^[A-Z_]+$')
        self._separatorPattern = re.compile(r'\s*\+')
        self._eolCommentPattern = re.compile(r'\s*#.*')

    def parseBnfSpec(self, lines):
        return BnfSpec(list(self.parseBnfRules(lines)))

    def parseBnfRules(self, lines):
        for line in lines:
            yield self.parseBnfRule(line)

    def parseBnfRule(self, line):
        lhs, rhs, op = self.splitRule(line)
        leftHandSymbol = self.parseNonterminal(lhs)
        rightHandSymbols, separator = self.parserRhs(rhs)
        return self.makeBnfRule(line, leftHandSymbol, op, rightHandSymbols, separator)

    def splitRule(self, line):
        m = self._rulePattern.match(line.string)
        if not m:
            raise self._MissingDefinitionOperator()
        lhs, op, rhs = m['lhs'], m['op'], m['rhs']
        return lhs, rhs, op

    class _MissingDefinitionOperator(Exception):
        pass

    def parseNonterminal(self, lhs):
        return NonterminalParser(self._symbolPattern, self._terminalPattern).parse(lhs)

    def parserRhs(self, rhs):
        return RightHandSideParser(
            self._symbolPattern,
            self._terminalPattern,
            self._separatorPattern,
            self._eolCommentPattern).parse(rhs)

    def makeBnfRule(self, line, leftHandSymbol, operator, rightHandSymbols, separator):
        return BnfRule(
            line=line,
            leftHandSymbol=leftHandSymbol,
            isRepeating=operator=='**=',
            rightHandSymbols=rightHandSymbols,
            separator=separator
        )

    def parseSymbol(self, matchScanner):
        return SymbolParser(self._symbolPattern, self._terminalPattern).parse(matchScanner)


class SymbolParser:
    def __init__(self, symbolPattern, terminalPattern):
        self._scanner = None
        self._symbolPattern = symbolPattern
        self._terminalPattern = terminalPattern

    def parse(self, matchScanner):
        self._scanner = matchScanner
        m = self._scanner.match(self._symbolPattern)
        if not m:
            raise self._InvalidSymbol()
        name = m['name']
        isCapture = bool(m['angle'])
        isTerminal = not isCapture or bool(self._terminalPattern.match(name))
        alt = '' if not isCapture else m['alt']
        return Symbol(isTerminal=isTerminal, name=name, alt=alt, isCapture=isCapture)

    class _InvalidSymbol(Exception):
        pass


class NonterminalParser(SymbolParser):
    def parse(self, string):
        symbol = self.parseSymbol(MatchScanner(string))
        if symbol.isTerminal:
            raise self._InvalidNonterminal()
        return symbol

    def parseSymbol(self, matchScanner):
        return SymbolParser(self._symbolPattern, self._terminalPattern).parse(matchScanner)

    class _InvalidNonterminal(Exception):
        pass


class RightHandSideParser:
    def __init__(self, symbolPattern, terminalPattern, separatorPattern, eolCommentPattern):
        self._symbolPattern = symbolPattern
        self._terminalPattern = terminalPattern
        self._separatorPattern = separatorPattern
        self._eolCommentPattern = eolCommentPattern

    def parse(self, string):
        scanner = MatchScanner(string)
        symbols = self.parseRightHandSymbols(scanner)
        sep = self.parseSeparator(scanner)
        self.parseEolComment(scanner)
        if scanner.hasMore():
            raise self._ExtraContent(scanner.getRemainder())
        return (symbols, sep)

    class _ExtraContent(Exception):
        pass

    def parseRightHandSymbols(self, scanner):
        symbols = []
        try:
            while True:
                symbols.append(self.parseSymbol(scanner))
        except SymbolParser._InvalidSymbol:
            pass
        return symbols

    def parseSeparator(self, matchScanner):
        m = matchScanner.match(self._separatorPattern)
        if m:
            symbol = BnfParser().parseSymbol(matchScanner)
            return symbol
        return None

    def parseSymbol(self, matchScanner):
        return SymbolParser(self._symbolPattern, self._terminalPattern).parse(matchScanner)

    def parseEolComment(self, matchScanner):
        m = matchScanner.match(self._eolCommentPattern)
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


MissingDefinitionOperator = BnfParser._MissingDefinitionOperator
InvalidNonterminal = NonterminalParser._InvalidNonterminal
InvalidSymbol = SymbolParser._InvalidSymbol
ExtraContent = RightHandSideParser._ExtraContent
