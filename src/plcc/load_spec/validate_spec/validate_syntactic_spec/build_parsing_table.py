from collections import defaultdict

class Table:
    def __init__(self):
        self._table = defaultdict(set)

    def get(self, X, a):
        return self._table[(X,a)]

    def set(self, X, a, rhs):
        self._table[(X, a)] = {rhs}

    def add(self, X, a, rhs):
        self._table[(X, a)].add(rhs)

def build_parsing_table(first: dict[str, set[str]], follow: dict[str, set[str]]): # -> Table: dict[(str, str): set[str]]
    table = Table()
    for X in first:
        for t in first[X]:
            for item in first[X]:
                table.add(X, t, item)
    return table







