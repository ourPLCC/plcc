from dataclasses import dataclass


@dataclass(frozen=True)
class Line:
    string: str
    number: int
    file: str = None


def parse_lines(string, start=1, file=None, Line=Line):
    '''
    Yield Lines in string. Newlines are not preserved.

        string: The string from which Lines are parsed.
        start: Starting number for Line numbering (default=1).
        file: File stored in each Line.
        Line: Line constructor. Called like: Line(string=s, number=i, file=file)
    '''
    if string is None:
        return
    for i, s in enumerate(string.splitlines(), start=start):
        yield Line(string=s, number=i, file=file)
