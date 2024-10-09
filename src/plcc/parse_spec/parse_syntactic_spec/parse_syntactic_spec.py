from typing import List
from plcc.load_spec.load_rough_spec.parse_dividers import Divider
from plcc.load_spec.load_rough_spec.parse_lines import Line
import re
from re import Match
from .structs import (
    SyntacticSpec,
    SyntacticRule,
    Symbol,
    CapturingTerminal,
    RepeatingSyntacticRule,
    StandardSyntacticRule,
    LhsNonTerminal,
    RhsNonTerminal,
    Terminal,
    CapturingSymbol,
    MalformedLHSError,
    MalformedBNFError,
)


def parse_syntactic_spec(lines: List[Line | Divider] | None) -> SyntacticSpec:
    return SyntacticParser(lines).parseSpec()


class SyntacticParser:
    def __init__(self, input: List[Line | Divider] | None):
        self.spec = SyntacticSpec()
        self.lines = input

    def parseSpec(self) -> SyntacticSpec:
        if not self.lines:
            return self.spec
        for line in self.lines[1:]:
            parser = SyntacticLineParser(line)
            if parser.isSyntacticRule():
                self.spec.append(parser.parseSyntacticRule())
        return self.spec


class SyntacticLineParser:

    def __init__(self, line: Line):
        self.line = line
        self.lhs = None
        self.rhs = None
        self.separator = None

    def parseSyntacticRule(self) -> SyntacticRule:
        standard, separated, repeating = self._buildMatches()
        if standard:
            return self._parseStandardRule(standard)
        elif separated:
            return self._parseSeparatedRule(separated)
        elif repeating:
            return self._parseRepeatingRule(repeating)
        raise MalformedBNFError(self.line)

    def _parseStandardRule(self, standard: Match[str]) -> StandardSyntacticRule:
        self.lhs, self.rhs = standard["lhs"], standard["rhs"]
        return StandardSyntacticRule(self.line, self._parseLeft(), self._parseRight())

    def _parseLeft(self) -> LhsNonTerminal:
        match = self._matchLeft()
        if not match:
            raise MalformedLHSError(self.line)
        return LhsNonTerminal(match["nonTerminal"], match["altName"])

    def _parseRight(self) -> List[Symbol]:
        if self.rhs is None:
            return []
        return [
            self._parseSymbol(symbol)
            for symbol in self.rhs.split()
            if symbol and not symbol.startswith("#")
        ]

    def _parseSymbol(self, symbol: str) -> Symbol:
        capturing = re.match(r"<(?P<name>\S*)>(?P<altName>\S+)?", symbol)
        return (
            self._parseCapturing(capturing["name"], capturing["altName"])
            if capturing
            else Terminal(symbol)
        )

    def _parseCapturing(self, name: str, altName: str) -> CapturingSymbol:
        terminal = re.match(r"[A-Z_]+", name)
        altName = altName.strip(":") if altName is not None else altName
        return (
            CapturingTerminal(name, altName)
            if terminal
            else RhsNonTerminal(name, altName)
        )

    def _buildMatches(
        self,
    ) -> tuple[Match[str] | None, Match[str] | None, Match[str] | None]:
        lineStr = self.line.string.split("#")[0].strip()
        standard = re.match(
            r"^\s*(?P<lhs><\S+>(?::\S+)?)\s*::=(?:\s(?P<rhs>.*))?", lineStr
        )
        separated = re.match(
            r"^\s*(?P<lhs><\S+>(?::\S+)?)\s*\*\*=\s(?P<rhs>.*)(?P<separator>\+.*)",
            lineStr,
        )
        repeating = re.match(
            r"^\s*(?P<lhs><\S+>(?::\S+)?)\s*\*\*=\s(?P<rhs>.*)", lineStr
        )
        return standard, separated, repeating

    def _parseSeparatedRule(self, separated: Match[str]) -> RepeatingSyntacticRule:
        self.lhs, self.rhs, self.separator = (
            separated["lhs"],
            separated["rhs"],
            separated["separator"].strip("+").strip(" "),
        )
        return self._parseRepeating()

    def _parseRepeatingRule(self, repeating: Match[str]) -> RepeatingSyntacticRule:
        self.lhs, self.rhs = repeating["lhs"], repeating["rhs"]
        return self._parseRepeating()

    def _parseRepeating(self) -> RepeatingSyntacticRule:
        return RepeatingSyntacticRule(
            self.line,
            self._parseLeft(),
            self._parseRight(),
            Terminal(self.separator) if self.separator else None,
        )

    def _matchLeft(self) -> Match[str] | None:
        return re.match(r"<(?P<nonTerminal>\S*)>(?::(?P<altName>\S+))?\s*", self.lhs)

    def isSyntacticRule(self) -> bool:
        return re.match(
            r"^\s*$", self.line.string
        ) is None and not self.line.string.startswith("#")
