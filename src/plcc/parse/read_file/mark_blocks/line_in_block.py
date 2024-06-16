from dataclasses import dataclass


from ..read_lines import Line


@dataclass(frozen=True)
class LineInBlock(Line):
    isInBlock: bool = True


def markLineInBlock(line):
    if not isInBlock(line):
        return LineInBlock(string=line.string, number=line.number, file=line.file, isInBlock=True)
    else:
        return line


def isInBlock(line):
    try:
        return line.isInBlock
    except:
        return False


