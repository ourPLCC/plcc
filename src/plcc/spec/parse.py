from .section import parseSections
from .lexical import parseLexicalSpec
from .syntactic import parseSyntacticSpec
from .semantic import parseSemanticSpec


def parseSpec(specLines):
    sections = parseSections(lines)
    lex = parseLexicalSpec(sections[0])
    syntax = parseSyntacticSpec(sections[1])
    semJava = parseSemantics(sections[2])
    semPython = parseSemantics(sections[3])
    return Spec(
        lex,
        syntax,
        semJava,
        semPython
    )
