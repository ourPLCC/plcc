class LexicalSpec():
    def __init__(self, termSpecs, termSet):
        self._termSpecs = termSpecs.copy()
        self._termSet = termSet.copy()

    def isTerminal(self, candidate):
        return candidate in self._termSet
