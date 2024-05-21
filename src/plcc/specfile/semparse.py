from __future__ import annotations
from dataclasses import dataclass


class SemParser:
    def parse(self, lines):
        for line in lines:
            if line.isInBlock:
                code.appends(line.string)
        ...


@dataclass
class SemRule:
    ...
