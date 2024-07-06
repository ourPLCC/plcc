from __future__ import annotations
from typing import Callable


from .include import Include
from plcc.visitor_pattern import Transformation, Transform


class LinesToIncludes(Transformation):
    def __init__(self, Include: Callable[[], Include]=Include):
        super().__init__(visitor=IncludeTransform(Include))


class IncludeTransform(Transform):
    def visit_Line(self, line):
        if self.isInclude(line):
            file = self.getFile(line)
            return Include(file=file, line=line)
        else:
            return line
