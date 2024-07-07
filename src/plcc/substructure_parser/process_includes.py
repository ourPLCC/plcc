from pathlib import Path


from .parse_lines import parse_lines
from .parse_blocks import parse_blocks
from .parse_includes import parse_includes, Include


class CircularIncludeError(Exception):
    def __init__(self, line):
        self.line = line


def parse_file(file):
    return parse_includes(
        parse_blocks(
            parse_lines(
                read_file(file),
                file=file
            )
        )
    )


def read_file(file):
    with open(file, 'r') as f:
        return f.read()


def process_includes(lines, parse_file=parse_file):
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
        for line in self.process(self.parse_file(p)):
            yield line
        self.seen.pop()

