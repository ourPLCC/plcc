from collections import defaultdict
# an addition parameter of
# impossible, because how would we know how to map cS to B
class Table:
    def __init__(self):
        self._table = defaultdict(list)

    def get(self, X, a):
        return self._table[(X,a)]

    def set(self, X, a, rhs):
        self._table[(X, a)] = {rhs}

    def add(self, X, a, rhs):
        self._table[(X, a)].append({rhs})

def build_parsing_table(first: dict[str, set[str]], follow: dict[str, set[str]], rules: dict[str, list[str]]): # -> Table: dict[(str, str): list[set[str]]]
    return ParsingTableBuilder(first, follow, rules).build()

class ParsingTableBuilder:
    def __init__(self, first, follow, rules):
        self.first = first
        self.follow = follow
        self.rules = rules
        self.table = Table()

    def build(self):
        self._addFirstSetRules()
        return self.table

    def _addFirstSetRules(self):
        for nonterminal in self.rules.keys():
            for productionLists in self.rules[nonterminal]:
                for production in productionLists:
                    if self._isNonterminalOnly(production) and self._isProductionInNonterminalsRule(production, nonterminal):
                        continue
                    for t in self.first[production]:
                        self.table.add(nonterminal, t, production)

                    if self._isEpsilonInSet(self.first[production]):
                        for t in self.follow[nonterminal]:
                            self.table.add(nonterminal, t, production)

# epsilon is both a production and t

    def _addFollowSetRules(self, nonterminal, production):
        for t in self.follow[production]:
            self.table.add(nonterminal, t, production)


    def _isNonterminalOnly(self, production):
        return True if production in self.rules.keys() else False


    def _isProductionInNonterminalsRule(self, production, nonterminal):
        return True if production in self.rules[nonterminal] else False

    def _isEpsilonInSet(self, production):
        return True if '' in production else False














