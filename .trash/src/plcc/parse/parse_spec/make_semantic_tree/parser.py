from __future__ import annotations
from abc import ABC, abstractmethod
import re


from ...read_sections import Line, Block


def parse(builder: Builder, lines: str|[str]|[Line|Block]) -> None:
    blank_line = re.compile(r'^\s*$')
    comment_line = re.compile(r'^\s*#.*$')
    header_line = re.compile(r'^(?P<module>\w+)(?::(?P<location>\w+))?\s*(?:#.*)?$')

    builder.begin()
    lines = Line.asLines(lines)
    for line in lines:

        if isinstance(line, Block):
            builder.setCode(line.lines)
            continue
        else:
            s = line.string
            m = blank_line.match(s)
            if m:
                continue
            m = comment_line.match(s)
            if m:
                continue
            m = header_line.match(s)
            if m:
                builder.startBlock(m['module'], m['location'], line)
                continue

    builder.end()


class Builder(ABC):
    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    def startBlock(self, module:str, location:str, line: Line) -> None:
        ...

    @abstractmethod
    def setCode(self, lines: [Line]) -> None:
        ...

    @abstractmethod
    def end(self) -> None:
        ...


class SemanticParseError(Exception):
    def __init__(self, line):
        self.line = line
