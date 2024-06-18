import re


class UnrecognizedError(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column


def parse_syntactic_section(builder, section):
    blank_line = re.compile(r'^\s*$')
    comment = re.compile(r'\s*#.*')
    define = re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<dis>\w*)|)\s*(?P<op>::=|\*\*=)')
    separator = re.compile(r'\s*\+\s*(?P<name>[A-Z_]+)')
    terminal = re.compile(r'\s*(?P<name>[A-Z_]+)')
    capturing_terminal = re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<dis>\w*)|)')
    nonterminal = re.compile(r'\s*(?P<angle><)?(?P<name>\w+)(?(angle)>:?(?P<dis>\w*)|)')
    comment = re.compile(r'\s*#.*')

    builder.begin()
    k = 1 # skip divider line (%)
    lines = section.lines
    while k < len(lines):
        line = lines[k]
        string = line.string
        i = 0
        while i < len(string):
            string = line.string
            m = blank_line.match(string)
            if m:
                i += len(m[0])
                continue

            m = comment.match(string)
            if m:
                i += len(m[0])
                continue

            m = define.match(string)
            if m:
                if m['op'] == '**=':
                    self.builder.startRepeatingRule(m['name'], m['dis'], line, i+1)
                else:
                    self.builder.startStandardRule(m['name'], m['dis'], line, i+1)

            m = separator.match(string, i)
            if m:
                self.builder.setSeparator(m['name'], line, i+1)
                i += len(m[0])
                continue

            m = terminal.match(string, i)
            if m:
                self.builder.addTerminal(m['name'], line, i+1)
                i += len(m[0])
                continue

            m = capturing_terminal.match(string, i)
            if m:
                self.builder.addCapturingTerminal(m['name'], m['dis'], line, i+1)
                i += len(m[0])
                continue

            m = nonterminal.match(string, i)
            if m:
                self.builder.addNonterminal(m['name'], m['dis'], line, i+1)
                i += len(m[0])
                continue

            raise UnrecognizedError(line, i+1)

        k += 1

    builder.end()
