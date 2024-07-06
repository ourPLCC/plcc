from pathlib import Path


def read_file(path):
    with Path(path).open('r') as f:
        return f.read()
