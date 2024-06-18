from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass
class Section:
    content: [Line|Block]


@dataclass
class Block:
    lines: [Line]


@dataclass(frozen=True)
class Line:
    string: str
    number: int
    file: Path

    @staticmethod
    def asLines(obj):
        if isinstance(obj, str):
            return [Line(s, i, None) for i, s in enumerate(obj.splitlines(), start=1)]
        elif isinstance(obj, list):
            if isinstance(obj[0], str):
                return [Line(s, i, None) for i, s in enumerate(obj, start=1)]
            elif isinstance(obj[0], Line):
                return obj
        raise TypeError(f'Unsupported type: {type(obj)}')


def read_sections(file):
    file = str(Path(file).resolve())
    return section(include(file))


def section(linesOrBlocks, divider_pat=re.compile(r'^%(?:\s+.*)?$')):
    section_content = []
    sections = []
    for lob in linesOrBlocks:
        if isinstance(lob, Block):
            section_content.append(lob)
        else:
            line = lob
            m = divider_pat.match(line.string)
            if m:
                sections.append(Section(section_content))
                section_content = [line]
            else:
                section_content.append(line)
    sections.append(Section(section_content))
    return sections


def include(
        file,
        read_lines_fn=lambda f: identify_blocks(make_lines(f, read_strings(f))),
        disable_fn=lambda x: isinstance(x, Block),
        include_pat=re.compile(r'^%include\s+(?P<path>.*)')
    ):
    stack = []
    file = str(Path(file).resolve())
    return _include(stack, file, read_lines_fn, disable_fn, include_pat)


def _include(stack, file, read_lines_fn, disable_fn, include_pat, line=None):
    file = Path(file)
    out = []
    if file in stack:
        raise CircularIncludeError(line)
    stack.append(file)
    for line in read_lines_fn(str(file)):
        if disable_fn(line):
            out.append(line)
        else:
            m = include_pat.match(line.string)
            if m:
                p = Path(m['path'])
                if not p.is_absolute():
                    p = (file.parent/p).resolve()
                out.extend(_include(stack, str(p), read_lines_fn, disable_fn, include_pat, line))
            else:
                out.append(line)
    stack.pop()
    return out


def identify_blocks(lines, brackets={'%%%':'%%%','%%{':'%%}'}):
    close = None
    blockLines = None
    out = []
    for line in lines:
        if close is None and line.string in brackets:
            close = brackets[line.string]
            blockLines = [line]
        elif close is not None and line.string == close:
            blockLines.append(line)
            b = Block(blockLines)
            out.append(b)
            close = None
            blockLines = None
        elif close is not None:
            blockLines.append(line)
        else:
            out.append(line)
    if blockLines is not None:
        raise UnclosedBlockError(blockLines[0])
    return out


def make_lines(file, strings):
    return [Line(string, number, file) for number, string in enumerate(strings, start=1)]


def read_strings(file):
    with open(file, 'r') as f:
        return f.read().splitlines()


class CircularIncludeError(Exception):
    def __init__(self, line):
        self.line = line
