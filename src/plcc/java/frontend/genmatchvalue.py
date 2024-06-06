from plcc.spec.parser.specreader import SpecReader
from plcc.spec.parser.lexparser import LexParser


def genMatchValue(rule):
    lexspec = LexParser().parseIntoLexSpec(SpecReader().readLinesFromString(rule))
    r = lexspec.rules[0]
    if r.isToken:
        s = f'{r.name} ("{r.pattern}")'
    else:
        s = f'{r.name} ("{r.pattern}", TokType.SKIP)'
    return s.replace('\\', '\\\\')
