from __future__ import annotations

from dataclasses import dataclass
from .parse_lines import Line
from .parse_dividers import Divider
from .parse_blocks import Block


def split_rough_spec(rough_spec:list) -> RoughSpec:
    return RoughSpecSplitter().split(rough_spec)


@dataclass
class RoughSpec:
    lexicalSection: list[Line]
    syntacticSection: list[Line | Divider]
    semanticSectionList: list[list[Line | Divider | Block]]


class RoughSpecSplitter:
    def __init__(self):
        self._roughSpec = None
        self._sectionList = None

    def split(self, rough_spec:list) -> RoughSpec:
        self._reset(rough_spec)
        self._splitElementsIntoSectionsByDividers()
        return self._makeRoughSpec()

    def _reset(self, rough_spec):
        self._roughSpec = rough_spec
        self._sectionList = [[]]

    def _splitElementsIntoSectionsByDividers(self):
        for el in self._roughSpec:
            if isinstance(el, Divider):
                self._sectionList.append([el])
            else:
                self._sectionList[-1].append(el)

    def _makeRoughSpec(self):
        tmpLexical, tmpSyntactic, tmpSemanticList = self._getSections()
        return RoughSpec(
            lexicalSection=tmpLexical,
            syntacticSection=tmpSyntactic,
            semanticSectionList=tmpSemanticList
        )

    def _getSections(self):
        tmpLexical = self._sectionList[0]
        tmpSyntactic = self._sectionList[1] if len(self._sectionList) > 1 else []
        tmpSemanticList = self._sectionList[2:] if len(self._sectionList) > 2 else []
        return tmpLexical, tmpSyntactic, tmpSemanticList
