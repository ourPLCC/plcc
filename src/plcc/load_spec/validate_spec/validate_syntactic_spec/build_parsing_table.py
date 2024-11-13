from collections import defaultdict

class Table:
    def __init__(self):
        self._table = defaultdict(list)

    def get(self, X: str, a: str) -> list[set[str]]:
        return self._table[(X,a)]

    def set(self, X, a, rhs):
        self._table[(X, a)] = {rhs}

    def add(self, X:str, a:str, rhs:str):
        self._table[(X, a)].append({rhs})

    def getKeys(self) -> list[tuple[str, str]]:
        return list(self._table.keys())

    def getValues(self):
        return list(self._table.values())

def build_parsing_table(first: dict[str, set[str]], follow: dict[str, set[str]], rules: dict[str, list[str]]) -> Table:
    return ParsingTableBuilder(first, follow, rules).build()

class ParsingTableBuilder:
    def __init__(self, first, follow, rules):
        self.first = first
        self.follow = follow
        self.rules = rules
        self.table = Table()

    def build(self):
        self._addRulesToCorrectCells()
        return self.table

    def _addRulesToCorrectCells(self):
        for nonterminal in self.rules.keys():
            for productionLists in self.rules[nonterminal]:

                for production in productionLists:
                    if self._isNonterminalOnly(production) and self._isProductionInNonterminalsRule(production, nonterminal):
                        continue
                    self.addFirstSetRulesIfValid(nonterminal, production)

                    if self._isEpsilonInSet(self.first[production]):
                        self._addFollowSetRulesIfValid(nonterminal, production)

    def addFirstSetRulesIfValid(self, nonterminal: str, production: str):
        for t in self.first[production]:
            if self._isTerminalEpisilon(t):
                continue
            self.table.add(nonterminal, t, production)

    def _addFollowSetRulesIfValid(self, nonterminal: str, production: str):
        for t in self.follow[nonterminal]:
            if self._isTerminalEpisilon(t):
                continue
            self.table.add(nonterminal, t, production)

    def _isTerminalEpisilon(self, t: str):
        return True if t == "" else False

    def _isNonterminalOnly(self, production):
        return True if production in self.rules.keys() else False


    def _isProductionInNonterminalsRule(self, production: str, nonterminal: str):
        return True if production in self.rules[nonterminal] else False

    def _isEpsilonInSet(self, s: set):
        return True if '' in s else False
