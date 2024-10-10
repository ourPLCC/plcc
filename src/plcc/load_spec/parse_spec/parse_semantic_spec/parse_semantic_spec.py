from dataclasses import dataclass
from .parse_code_fragments import CodeFragment, parse_code_fragments
from plcc.load_spec.load_rough_spec.parse_lines import Line
from plcc.load_spec.load_rough_spec.parse_blocks import Block
from plcc.load_spec.load_rough_spec.parse_dividers import Divider
import re

@dataclass
class SemanticSpec:
    language: str
    tool: str
    codeFragmentList: [CodeFragment]

def parse_semantic_spec(semantic_spec: list[Divider | Line | Block]) -> SemanticSpec:
    divider = semantic_spec[0]
    codeFragmentList = parse_code_fragments(semantic_spec[1:])
    return SemanticSpec(language = divider.language, tool = divider.tool, codeFragmentList=codeFragmentList)

