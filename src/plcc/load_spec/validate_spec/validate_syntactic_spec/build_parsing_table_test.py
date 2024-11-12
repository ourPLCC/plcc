from pytest import raises
from .build_parsing_table import build_parsing_table, Table
from collections import defaultdict

def test_first_set_placement():
    firstSets = buildBasicFirstSet()
    followSets = buildBasicFollowSet()
    rules = buildBasicRules()
    table = build_parsing_table(firstSets, followSets, rules)
    assert table.get('s', 'C') == [{"b C"}, {'d b'}]
    assert table.get('s', 'A') == [{"b C"}, {'d b'}]
    assert table.get('s', 'D') == [{"d b"}]
    assert table.get('b', 'A') == [{"A B"}]
    assert table.get('b', 'C') == [{"C s"}]
    assert table.get('d', 'A') == [{""}]
    assert table.get('d', 'C') == [{""}]
    assert table.get('d', 'D') == [{"D"}]

def buildBasicFirstSet():
    firstSets = defaultdict(set)
    firstSets['d'] = {"D", ""}
    firstSets['b'] = {"A", "C"}
    firstSets['s'] = {"A", "C", "D"}
    firstSets['b C'] = {"A", "C"}
    firstSets['d b'] = {"D", "A", "C"}
    firstSets['A B'] = {"A"}
    firstSets['C s'] = {"C"}
    firstSets['D'] = {"D"}
    firstSets[""] = {""}

    return firstSets

def buildBasicFollowSet():
    followSets = defaultdict(set)
    followSets["d"] = {"A", "C"}
    followSets["b"] = {"C",chr(26)}
    followSets["s"] = {chr(26), "C"} #chr(26) is EOL

    return followSets

def buildBasicRules():
    rules = defaultdict(list)
    rules["s"] = [["b C", "d b"]]
    rules["b"] = [["A B", 'C s']]
    rules["d"] = [["D"],[""]]

    return rules

