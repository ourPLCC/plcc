from pathlib import Path
from .read import readSpecLines
from .parse import parseSpec


def load(specFile):
    return parseSpec(readSpecLines(Path(specFile)))
