from __future__ import annotations
from dataclasses import dataclass
import re


from .semrule import SemRule


class SemParserPatterns:
    def __init__(self):
        self.class_ = re.compile(r'\s*(?P<class_>\w+)(?::(?P<modifier>\w+))?(?:\s*#.*)?')


class SemParser:
    def __init__(self, semParserPatterns=None):
        if not semParserPatterns:
            semParserPatterns = SemParserPatterns()
        self._patterns = semParserPatterns

    def parse(self, lines):
        for line in lines:
            m = self._patterns.class_.match(line.string)
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
