from __future__ import annotations
from dataclasses import dataclass
import re


from .semrule import SemRule


class SemParser:
    def __init__(self, semParserPatterns=None):
        self._classPattern=re.compile(r'^\s*(?P<class_>\w+)(?::(?P<modifier>\w+))?(?:\s*#.*)?$')

    def parse(self, lines):
        for line in lines:
            m = self._classPattern.match(line.string)
            if not m:
                raise self.InvalidSemRule()
            next(lines)
            line = next(lines)
            codeBlock = []
            while line.isInCodeBlock:
                codeBlock.append(line)
                line = next(lines)
            yield SemRule(class_=m['class_'], modifier=m['modifier'], code=codeBlock)

    class InvalidSemRule(Exception):
        pass
