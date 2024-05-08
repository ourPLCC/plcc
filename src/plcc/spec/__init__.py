from pathlib import Path


from .parse.read import readSpecLines
from .parse.spec import parseSpec


def load(specFile):
    return parseSpec(readSpecLines(Path(specFile)))
