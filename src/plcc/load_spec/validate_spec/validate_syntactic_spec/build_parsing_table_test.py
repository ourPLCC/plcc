from pytest import raises
from .build_parsing_table import build_parsing_table, Table
from collections import defaultdict

def test_basic():
    firstSets = buildBasicFirstSet()
    followSets = buildBasicFollowSet()
    table = build_parsing_table(firstSets, followSets)
    assert table.get('s', 'A') == {"A", "C", "D"}

def buildBasicFirstSet():
    firstSets = defaultdict(set)
    firstSets['s'] = {"A", "C", "D"}
    firstSets['b'] = {"A", "C"}
    firstSets['d'] = {"D", ""}
    return firstSets

def buildBasicFollowSet():
    followSets = defaultdict(set)
    followSets["s"] = {chr(26), "C"} #chr(26) is EOL
    followSets["b"] = {chr(26), "C"}
    followSets["d"] = {"A", "C"}
    return followSets

