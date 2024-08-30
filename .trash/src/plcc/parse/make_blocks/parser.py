from __future__ import annotations
from abc import ABC, abstractmethod
import re


def parse(builder, lines: [Line]) -> None:
    ppp = re.compile(r'^%%%(?:\s*#.*)?')
    ppL = re.compile(r'^%%{(?:\s*#.*)?')
    ppR = re.compile(r'^%%}(?:\s*#.*)?')
    brackets = {
        ppp: ppp,
        ppL: ppR
    }
    seekingClose = None

    lines = [] if lines is None else lines
    builder.begin()
    for line in lines:
        if seekingClose:
            m = seekingClose.match(line.string)
            if m:
                builder.close(line)
                seekingClose = None
            else:
                builder.line(line)
            continue

        m = None
        for open in brackets:
            m = open.match(line.string)
            if m:
                break
        if m:
            seekingClose = brackets[open]
            builder.open(line)
            continue
        else:
            builder.line(line)
            continue


class Builder(ABC):
    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    def open(self, line: Line) -> None:
        ...

    @abstractmethod
    def line(self, line: Line) -> None:
        ...

    @abstractmethod
    def close(self, line: Line) -> None:
        ...

    @abstractmethod
    def end(self) -> None:
        ...
