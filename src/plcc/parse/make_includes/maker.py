from .parser import parse
from .builder import Builder


def make_includes(self, lines):
    return IncludeTransformation().visit(lines)
