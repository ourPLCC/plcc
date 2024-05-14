from __future__ import annotations
from typing import Iterable


from ..specfile.line import Line


def parse(lines: Iterable[Line]) -> Spec:
    ...


def Spec():
    def parse(self, lines: Iterable[Line]):
        ...

    def getSectionCount(self):
        return 3
