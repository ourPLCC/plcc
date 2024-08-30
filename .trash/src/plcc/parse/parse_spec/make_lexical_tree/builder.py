from __future__ import annotations
from overrides import override


from .tree import TokenRule
from .tree import SkipRule
from .tree import LexicalTree


from .parser import Builder, parse


class LexicalTreeBuilder(Builder):
    @override
    def begin(self):
        self.result = None
        self.rules = []

    @override
    def addTokenRule(self, name, pattern, line):
        self.rules.append(TokenRule(name, pattern, line))

    @override
    def addSkipRule(self, name, pattern, line):
        self.rules.append(SkipRule(name, pattern, line))

    @override
    def end(self):
        self.result = LexicalTree(self.rules)
