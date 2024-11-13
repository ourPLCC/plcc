from pytest import raises
from .build_parsing_table import build_parsing_table, Table
from collections import defaultdict
def test_empty():
    firstSets = buildFirstSet([],[])
    followSets = buildFollowSet([],[])
    rules = buildRules([],[])

    table = build_parsing_table(firstSets, followSets, rules)
    assert len(table.getKeys()) == 0

def test_complex_not_LL1():
    productions = ['d', 'b', 's', 'b C', 'd b', 'A B', 'C s', 'D', ""]
    firstOfProductions = [{"D", ""}, {"A", "C"}, {"A", "C", "D"}, {"A", "C"}, {"D", "A", "C"}, {"A"}, {"C"}, {"D"}, {""}]
    followOfProductions = [{"A", "C"}, {"C", chr(26)}, {chr(26), "C"}]

    firstSets = buildFirstSet(productions, firstOfProductions)
    followSets = buildFollowSet(productions, followOfProductions)

    lhs = ["s", "b", "d"]
    rhs = [["b C", "d b"],["A B", 'C s'],["D", ""]]
    rules = buildRules(lhs, rhs)

    table = build_parsing_table(firstSets, followSets, rules)
    assert table.get('s', 'C') == [{"b C"}, {'d b'}]
    assert table.get('s', 'A') == [{"b C"}, {'d b'}]
    assert table.get('s', 'D') == [{"d b"}]
    assert table.get('b', 'A') == [{"A B"}]
    assert table.get('b', 'C') == [{"C s"}]
    assert table.get('d', 'A') == [{""}]
    assert table.get('d', 'C') == [{""}]
    assert table.get('d', 'D') == [{"D"}]
    assert len(table.getKeys()) == 8


def buildFirstSet(productions: list[str], firstOfProductions: list[set[str]]) -> dict[str, set[str]]:
    firstSets = defaultdict(set)
    for i, production in enumerate(productions):
        firstSets[production] = firstOfProductions[i]
    return firstSets

def buildFollowSet(productions: list[str], followOfProductions: list[set[str]]) -> dict[str, set[str]]:
    followSets = defaultdict(set)
    for i, production in enumerate(productions):
        try:
            followSets[production] = followOfProductions[i]
        except:
            break
    return followSets

def buildRules(lhs: list[str], rhs: list[list[str]]) -> dict[str, list[list[str]]]:
    rules = defaultdict(list)
    for i, nonterminal in enumerate(lhs):
        rules[nonterminal] = [rhs[i]]
    return rules
