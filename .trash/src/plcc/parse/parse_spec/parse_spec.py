
from dataclasses import dataclass


from ..read_sections import read_sections


@dataclass
class Spec:
    lexicalSpec: LexicalSpec
    syntacticSpec: SyntacticSpec
    semanticSpecs: [SemanticSpec]


def parse_spec(file):
    sections = read_sections(file)
    sections, lexical_spec = parse_section(sections, LexicalSpecBuilder, parse_lexical_section)
    sections, syntactic_spec = parse_section(sections, SyntacticSpecBuilder, parse_syntactic_section)
    semantic_specs = parse_all_sections(sections, SemanticSpecBuilder, parse_semantic_section)
    return Spec(lexical_spec, syntactic_spec, semantic_specs)


def parse_section(sections, Builder, parse_fn):
    if sections:
        s = sections[0]
        b = Builder()
        parse_fn(s, b)
        spec = b.spec
        return sections[1:], spec
    return sections, None


def parse_all_sections(sections, Builder, parse_fn):
    specs = []
    while sections:
        sections, spec = parse_section(sections, Builder, parse_fn)
        specs.append(spec)
    return specs
