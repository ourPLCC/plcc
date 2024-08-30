import re


class LexValidator:
    def validate(self, lexrules):
        self.namesAreUppercaseAndUnderscoreOnly(lexrules)
        self.noDuplicateNames(lexrules)
        self.noUnmatchedContentAtTheEndOfLines(lexrules)

    def namesAreUppercaseAndUnderscoreOnly(self, lexrules):
        uppersAndUnderscore = re.compile(r'^[A-Z_]+$')
        for rule in lexrules:
            if not uppersAndUnderscore.match(rule.name):
                raise self.InvalidName(rule.line)

    def noDuplicateNames(self, lexrules):
        names = set()
        for r in lexrules:
            if r.name in names:
                raise self.DuplicateName(r.line)
            names.add(r.name)

    def noUnmatchedContentAtTheEndOfLines(self, lexrules):
        endOfLine = re.compile(r'^\s*(?:#.*)?$')
        for r in lexrules:
            if not endOfLine.match(r.remainder):
                raise self.UnmatchedContent(r.line)

    class InvalidName(Exception):
        def __init__(self, line):
            self.line = line

    class DuplicateName(Exception):
        def __init__(self, line):
            self.line = line

    class UnmatchedContent(Exception):
        def __init__(self, line):
            self.line = line
