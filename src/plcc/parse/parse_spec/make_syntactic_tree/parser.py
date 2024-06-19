from __future__ import annotations


from abc import ABC, abstractmethod
import re


from ...read_sections import Line


def parse(builder, lines):
    blank_line = re.compile(r'^\s*$')
    comment = re.compile(r'\s*(#.*)')
    define = re.compile(r'\s*(<(?P<name>\w+)>(?::?(?P<dis>\w+)|)\s*(?P<op>::=|\*\*=))')
    separator = re.compile(r'\s*(\+\s*(?P<name>[A-Z_]+))')
    terminal = re.compile(r'\s*(?P<name>[A-Z_]+)')
    capturing_terminal = re.compile(r'\s*(<(?P<name>[A-Z_]+)>(?::?(?P<dis>\w+)|))')
    nonterminal = re.compile(r'\s*(<(?P<name>\w+)>(?::?(?P<dis>\w+)|))')

    lines = Line.asLines(lines)
    builder.begin()
    k = 1 # skip divider line (%)
    while k < len(lines):
        line = lines[k]
        string = line.string
        i = 0
        while i < len(string):
            string = line.string
            m = blank_line.match(string, i)
            if m:
                i += len(m[0])
                continue

            m = comment.match(string, i)
            if m:
                i += len(m[0])
                continue

            m = define.match(string, i)
            if m:
                column = getColumn(i, m)
                if m['op'] == '**=':
                    builder.startRepeatingRule(m['name'], m['dis'], line, column)
                else:
                    builder.startStandardRule(m['name'], m['dis'], line, column)
                i += len(m[0])
                continue

            m = separator.match(string, i)
            if m:
                column = getColumn(i, m)
                builder.setSeparator(m['name'], line, column)
                i += len(m[0])
                continue

            m = terminal.match(string, i)
            if m:
                column = getColumn(i, m)
                builder.addTerminal(m['name'], line, column)
                i += len(m[0])
                continue

            m = capturing_terminal.match(string, i)
            if m:
                column = getColumn(i, m)
                builder.addCapturedTerminal(m['name'], m['dis'], line, column)
                i += len(m[0])
                continue

            m = nonterminal.match(string, i)
            if m:
                column = getColumn(i, m)
                builder.addNonterminal(m['name'], m['dis'], line, column)
                i += len(m[0])
                continue

            raise ParseError(line, i+1)

        k += 1

    builder.end()


class ParseError(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column


def getColumn(i, m):
    return i + (len(m[0]) - len(m[1])) + 1


class Builder(ABC):
    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    def startRepeatingRule(self, name: str, disambiguation: str, line: Line, column: int) -> None:
        ...

    @abstractmethod
    def startStandardRule(self, name: str, disambiguation: str, line: Line, column: int) -> None:
        ...

    @abstractmethod
    def setSeparator(self, name: str, line: Line, column: int) -> None:
        ...

    @abstractmethod
    def addTerminal(self, name: str, line: Line, column: int) -> None:
        ...

    @abstractmethod
    def addCapturedTerminal(self, name: str, disambiguation: str, line: Line, column: int) -> None:
        ...

    @abstractmethod
    def addNonterminal(self, name: str, disambiguation: str, line: Line, column: int) -> None:
        ...

    @abstractmethod
    def end(self):
        ...
