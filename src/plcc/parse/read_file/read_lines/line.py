from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    string: str = ''
    number: int = 0
    file: str = ''


def toLines(strings, file=''):
    return [ Line(string=s, number=k, file=file) for k,s in enumerate(strings, start=1) ]
