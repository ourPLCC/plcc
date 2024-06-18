from .tree import TokenRule
from .tree import SkipRule
from .tree import LexicalTree


class LexicalTreeBuilder:
    def __init__(self):
        self.result = None
        self.rules = []

    def begin(self):
        self.result = None
        self.rules = []

    def addTokenRule(self, name, pattern, line):
        self.rules.append(TokenRule(name, pattern, line))

    def addSkipRule(self, name, pattern, line):
        self.rules.append(SkipRule(name, pattern, line))

    def end(self):
        self.result = LexicalTree(self.rules)



