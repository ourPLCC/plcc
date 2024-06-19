from overrides import override


from .parser import Builder


from .tree import SyntacticTree
from .tree import RepeatingRule
from .tree import StandardRule
from .tree import Defined
from .tree import Captured
from .tree import Uncaptured
from .tree import Terminal
from .tree import Nonterminal


class IllegalSeparatorError(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column


class SyntacticTreeBuilder(Builder):
    @override
    def begin(self):
        self.result = None
        self.rules = []

    @override
    def startRepeatingRule(self, name, disambiguation, line, column):
        self.rules.append(
            RepeatingRule(
                Defined(
                    Nonterminal(
                        name
                    ),
                    disambiguation,
                    line,
                    column
                ),
                symbols=[],
                separator=None
            )
        )

    @override
    def startStandardRule(self, name, disambiguation, line, column):
        self.rules.append(
            StandardRule(
                Defined(
                    Nonterminal(
                        name
                    ),
                    disambiguation,
                    line,
                    column
                ),
                symbols=[]
            )
        )

    @override
    def setSeparator(self, name, line, column):
        try:
            if self.rules[-1].separator:
                raise IllegalSeparatorError(line, column)
        except AttributeError:
            raise IllegalSeparatorError(line, column)
        self.rules[-1].separator = Uncaptured(Terminal(name), line, column)

    @override
    def addTerminal(self, name, line, column):
        self.rules[-1].symbols.append(Uncaptured(Terminal(name), line, column))

    @override
    def addCapturedTerminal(self, name, disambiguation, line, column):
        self.rules[-1].symbols.append(Captured(Terminal(name), disambiguation, line, column))

    @override
    def addNonterminal(self, name, disambiguation, line, column):
        self.rules[-1].symbols.append(Captured(Nonterminal(name), disambiguation, line, column))

    @override
    def end(self):
        self.result = SyntacticTree(self.rules)

