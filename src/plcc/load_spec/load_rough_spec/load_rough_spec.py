from pathlib import Path


from .parse_rough import parse_rough
from .parse_includes import Include
from .split_rough_spec import split_rough_spec


class CircularIncludeError(Exception):
    def __init__(self, line):
        self.line = line


def load_rough_spec(file):
    return split_rough_spec(
        process_includes(
            load_rough_spec_without_processing_includes(file)
    ))


def load_rough_spec_without_processing_includes(file):
    def read_file(file):
        with open(file, 'r') as f:
            return f.read()

    return parse_rough(
        string=read_file(file),
        file=file
    )


def process_includes(lines, parse_file=load_rough_spec_without_processing_includes):
    return IncludeProcessor(parse_file).process(lines)


class IncludeProcessor():
    def __init__(self, parse_file):
        self.parse_file = parse_file
        self.seen = []

    def process(self, lines):
        if lines is None:
            return []
        for line in lines:
            if isinstance(line, Include):
                yield from self.process_include(line)
            else:
                yield line

    def process_include(self, include):
        p = Path(include.file)
        if not p.is_absolute():
            if include.file.line is not None:
                p = (Path(include.line.file).parent/p).resolve()
            else:
                p = (Path.cwd()/p).resolve()
        p = str(p)
        if p in self.seen:
            raise CircularIncludeError(include.line)
        self.seen.append(p)
        yield from self.process(self.parse_file(p))
        self.seen.pop()
