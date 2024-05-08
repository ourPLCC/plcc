from pathlib import Path


from .read import readSpecLines
from .spec import parseSpec


def load(specFile):
    return parseSpec(readSpecLines(Path(specFile)))
