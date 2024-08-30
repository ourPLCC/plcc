from __future__ import annotations
from abc import ABC, abstractmethod


def parse(builder, strings: str|[str], file: str = None) -> None:
    if strings is None:
        strings = []
    if isinstance(strings, str):
        strings = strings.splitlines()
    builder.begin()
    builder.setFile(file)
    for s in strings:
        builder.line(s.rstrip('\n'))


class Builder(ABC):
    @abstractmethod
    def begin(self) -> None:
        ...

    @abstractmethod
    def setFile(self, file: str) -> None:
        ...

    @abstractmethod
    def line(self, string: str) -> None:
        ...

    @abstractmethod
    def end(self) -> None:
        ...
