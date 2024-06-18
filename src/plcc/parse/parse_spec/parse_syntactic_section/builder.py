from .tree import SyntacticTree
from .tree import RepeatingRule
from .tree import StandardRule
from .tree import Defining
from .tree import Capturing
from .tree import NonCapturing
from .tree import Terminal
from .tree import Nonterminal


class IllegalSeparatorError(Exception):
    def __init__(self, line, column):
        self.line = line
        self.column = column


class SyntacticTreeBuilder:
    def __init__(self):
        self.spec = None
        self.rules = []

    def begin(self):
        self.spec = None
        self.rules = []

    def startRepeatingRule(self, name, disambiguation, line, column):
        self.rules.append(
            RepeatingRule(
                Defining(
                    Nonterminal(
                        name
                    ),
                    disambiguation,
                    line,
                    column
                ),
                rhs=[],
                separator=None
            )
        )

    def startStandardRule(self, name, pattern, line, column):
        self.rules.append(
            StandardRule(
                Defining(
                    Nonterminal(
                        name
                    ),
                    disambiguation,
                    line,
                    column
                ),
                rhs=[]
            )
        )

    def setSeparator(self, name, line, column):
        try:
            if self.rules[-1].separator:
                raise IllegalSeparatorError(line, column)
        except AttributeError:
            raise IllegalSeparatorError(line, column)
        self.rules[-1].separator = NonCapturing(Terminal(name), line, column)

    def addTerminal(self, name, line, column):
        self.rules[-1].rhs.append(NonCapturing(Terminal(name), line, column))

    def addCapturingTerminal(self, name, disambiguation, line, column):
        self.rules[-1].rhs.append(Capturing(Terminal(name), disambiguation, line, column))

    def addNonterminal(self, name, disambiguation, line, column):
        self.rules[-1].rhs.append(Capturing(Nonterminal(name), disambiguation, line, column))

    def end(self):
        self.spec = SyntacticTree(self.rules)

