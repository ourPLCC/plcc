import re

from .builder import SyntacticTreeBuilder
from .tree import SyntacticTree
from ...read_sections import Line


class UnrecognizedError(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column


def parse(lines):
    builder = SyntacticTreeBuilder()
    _parse(builder, lines)
    tree = builder.result
    return tree


def getColumn(i, m):
    return i + (len(m[0]) - len(m[1])) + 1


def _parse(builder, lines):
    blank_line = re.compile(r'^\s*$')
    comment = re.compile(r'\s*(#.*)')
    define = re.compile(r'\s*(<(?P<name>\w+)>(?::?(?P<dis>\w+)|)\s*(?P<op>::=|\*\*=))')
    separator = re.compile(r'\s*(\+\s*(?P<name>[A-Z_]+))')
    terminal = re.compile(r'\s*(?P<name>[A-Z_]+)')
    capturing_terminal = re.compile(r'\s*(<(?P<name>[A-Z_]+)>(?::?(?P<dis>\w+)|))')
    nonterminal = re.compile(r'\s*(<(?P<name>\w+)>(?::?(?P<dis>\w+)|))')

    lines = [] if lines is None else Line.asLines(lines)
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

            raise UnrecognizedError(line, i+1)

        k += 1

    builder.end()
