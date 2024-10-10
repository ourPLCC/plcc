from pytest import raises, mark, fixture
from typing import List
from .parse_syntactic_spec import parse_syntactic_spec
from .structs import (
    CapturingTerminal,
    RepeatingSyntacticRule,
    StandardSyntacticRule,
    LhsNonTerminal,
    RhsNonTerminal,
    Terminal,
    MalformedBNFError,
    Symbol,
)
from plcc.load_spec.load_rough_spec.parse_lines import Line
from plcc.load_spec.load_rough_spec.parse_dividers import Divider, parse_dividers


def test_None_yields_nothing():
    assert list(parse_syntactic_spec(None)) == []


def test_empty_yields_nothing():
    assert list(parse_syntactic_spec([])) == []


def test_divider_yields_nothing():
    lines = [makeDivider()]
    assert list(parse_syntactic_spec(lines)) == []


def test_blank_rule():
    blank_rule = makeLine("<noun> ::=")
    lines = [makeDivider(), blank_rule]
    expected = [makeStandardSyntacticRule(blank_rule, makeLhsNonTerminal("noun"), [])]
    assert list(parse_syntactic_spec(lines)) == expected


def test_one_rule():
    rule = makeLine("<noun> ::= WORD")
    lines = [makeDivider(), rule]
    expected = [
        makeStandardSyntacticRule(
            rule, makeLhsNonTerminal("noun"), [makeTerminal("WORD")]
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_two_rules():
    rule = makeLine("<noun> ::= WORD")
    lines = [makeDivider(), rule, rule]
    expected_rule = makeStandardSyntacticRule(
        rule, makeLhsNonTerminal("noun"), [makeTerminal("WORD")]
    )
    expected = [expected_rule, expected_rule]
    assert list(parse_syntactic_spec(lines)) == expected


def test_comment_ignored():
    rule = makeLine("<noun> ::= WORD")
    lines = [
        makeDivider(),
        makeLine("# TODO: rewrite this entire codebase in x86 assembly"),
        rule,
    ]
    expected = [
        makeStandardSyntacticRule(
            rule, makeLhsNonTerminal("noun"), [makeTerminal("WORD")]
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_comment_trailing_ignored():
    trailing_comment = makeLine("<noun> ::= WORD # wow!")
    lines = [makeDivider(), trailing_comment]
    expected = [
        makeStandardSyntacticRule(
            trailing_comment,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_empty_ignored():
    rule = makeLine("<noun> ::= WORD")
    lines = [makeDivider(), makeLine(""), rule]
    expected = [
        makeStandardSyntacticRule(
            rule, makeLhsNonTerminal("noun"), [makeTerminal("WORD")]
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_space_ignored():
    rule = makeLine("<noun> ::= WORD")
    lines = [makeDivider(), makeLine(" "), rule]
    expected = [
        makeStandardSyntacticRule(
            rule, makeLhsNonTerminal("noun"), [makeTerminal("WORD")]
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_named_lhs_non_terminal():
    named_lhs_line = makeLine("<noun>:Name ::= WORD")
    lines = [makeDivider(), named_lhs_line]
    expected = [
        makeStandardSyntacticRule(
            named_lhs_line,
            makeLhsNonTerminal("noun", "Name"),
            [makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_two_terminals():
    double_terminal = makeLine("<noun> ::= WORD WORD")
    lines = [makeDivider(), double_terminal]
    expected = [
        makeStandardSyntacticRule(
            double_terminal,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_three_terminals():
    triple_terminal = makeLine("<noun> ::= WORD WORD WORD")
    lines = [makeDivider(), triple_terminal]
    expected = [
        makeStandardSyntacticRule(
            triple_terminal,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_rhs_non_terminal():
    rhs_non_terminal_line = makeLine("<noun> ::= WORD WORD <word>")
    lines = [makeDivider(), rhs_non_terminal_line]
    expected = [
        makeStandardSyntacticRule(
            rhs_non_terminal_line,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeRhsNonTerminal("word")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_rhs_middle_non_terminal():
    rhs_non_terminal_line = makeLine("<noun> ::= WORD <word> WORD")
    lines = [makeDivider(), rhs_non_terminal_line]
    expected = [
        makeStandardSyntacticRule(
            rhs_non_terminal_line,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeRhsNonTerminal("word"), makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_capturing_terminal():
    rhs_capturing_terminal = makeLine("<noun> ::= WORD WORD <WORD>")
    lines = [makeDivider(), rhs_capturing_terminal]
    expected = [
        makeStandardSyntacticRule(
            rhs_capturing_terminal,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeCapturingTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_repeating():
    repeating_line = makeLine("<noun> **= WORD WORD WORD")
    lines = [makeDivider(), repeating_line]
    expected = [
        makeRepeatingSyntacticRule(
            repeating_line,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
            None,
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_repeating_rhs_non_terminal():
    repeating_non_terminal = makeLine("<noun> **= WORD WORD <word>")
    lines = [makeDivider(), repeating_non_terminal]
    expected = [
        makeRepeatingSyntacticRule(
            repeating_non_terminal,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeRhsNonTerminal("word")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_repeating_capturing_terminal():
    repeating_capturing_terminal = makeLine("<noun> **= WORD WORD <WORD>")
    lines = [makeDivider(), repeating_capturing_terminal]
    expected = [
        makeRepeatingSyntacticRule(
            repeating_capturing_terminal,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeCapturingTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_repeating_separator():
    repeating_separated = makeLine("<noun> **= WORD WORD WORD +WORD")
    lines = [makeDivider(), repeating_separated]
    expected = [
        makeRepeatingSyntacticRule(
            repeating_separated,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
            separator=makeTerminal("WORD"),
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_named_rhs_non_terminal():
    named_rhs = makeLine("<noun> ::= WORD WORD <word>hello")
    lines = [makeDivider(), named_rhs]
    expected = [
        makeStandardSyntacticRule(
            named_rhs,
            makeLhsNonTerminal("noun"),
            [
                makeTerminal("WORD"),
                makeTerminal("WORD"),
                makeRhsNonTerminal("word", "hello"),
            ],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_colon_rhs_non_terminal():
    colon_rhs = makeLine("<noun> ::= WORD WORD <word>:hello")
    lines = [makeDivider(), colon_rhs]
    expected = [
        makeStandardSyntacticRule(
            colon_rhs,
            makeLhsNonTerminal("noun"),
            [
                makeTerminal("WORD"),
                makeTerminal("WORD"),
                makeRhsNonTerminal("word", "hello"),
            ],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_double_space():
    double_spaced = makeLine("<noun> ::= WORD WORD  WORD")
    lines = [makeDivider(), double_spaced]
    expected = [
        makeStandardSyntacticRule(
            double_spaced,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_trailing_space():
    trailing_space = makeLine("<noun> ::= WORD WORD WORD ")
    lines = [makeDivider(), trailing_space]
    expected = [
        makeStandardSyntacticRule(
            trailing_space,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_leading_space():
    leading_space = makeLine(" <noun> ::= WORD WORD WORD")
    lines = [makeDivider(), leading_space]
    expected = [
        makeStandardSyntacticRule(
            leading_space,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_inserted_lhs_space():
    inserted_lhs_space = makeLine("<program>      ::= <cmds> END")
    lines = [makeDivider(), inserted_lhs_space]
    expected = [
        makeStandardSyntacticRule(
            inserted_lhs_space,
            makeLhsNonTerminal("program"),
            [makeRhsNonTerminal("cmds"), makeTerminal("END")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_inserted_rhs_space():
    inserted_rhs_space = makeLine("<program> ::=  <cmds> END")
    lines = [makeDivider(), inserted_rhs_space]
    expected = [
        makeStandardSyntacticRule(
            inserted_rhs_space,
            makeLhsNonTerminal("program"),
            [makeRhsNonTerminal("cmds"), makeTerminal("END")],
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_spaced_separator():
    spaced_separator = makeLine("<noun> **= WORD WORD WORD  +WORD ")
    lines = [makeDivider(), spaced_separator]
    expected = [
        makeRepeatingSyntacticRule(
            spaced_separator,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD"), makeTerminal("WORD")],
            separator=makeTerminal("WORD"),
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_embedded_separator():
    embedded_separator = makeLine("<noun> **= WORD WORD +WORD WORD")
    lines = [makeDivider(), embedded_separator]
    expected = [
        makeRepeatingSyntacticRule(
            embedded_separator,
            makeLhsNonTerminal("noun"),
            [makeTerminal("WORD"), makeTerminal("WORD")],
            separator=makeTerminal("WORD WORD"),
        )
    ]
    assert list(parse_syntactic_spec(lines)) == expected


def test_malformed_bnf_raises():
    lines = [makeDivider(), makeLine("<noun> +*= WORD")]
    with raises(MalformedBNFError):
        parse_syntactic_spec(lines)


def makeDivider(string="%", lineNumber=0, file=""):
    return parse_dividers([makeLine(string, lineNumber, file)])


def makeLine(string, lineNumber=0, file: str = ""):
    return Line(string, lineNumber, file)


def makeLhsNonTerminal(name: str, alt_name: str | None = None):
    return LhsNonTerminal(name, alt_name)


def makeTerminal(name: str):
    return Terminal(name)


def makeRhsNonTerminal(name: str, alt_name: str | None = None):
    return RhsNonTerminal(name, alt_name)


def makeCapturingTerminal(name: str, alt_name: str | None = None):
    return CapturingTerminal(name, alt_name)


def makeStandardSyntacticRule(
    line: Line, lhs: LhsNonTerminal, rhsSymbolList: List[Symbol]
):
    return StandardSyntacticRule(line, lhs, rhsSymbolList)


def makeRepeatingSyntacticRule(
    line: Line,
    lhs: LhsNonTerminal,
    rhsSymbolList: List[Symbol],
    separator: Terminal | None = None,
):
    return RepeatingSyntacticRule(line, lhs, rhsSymbolList, separator)
