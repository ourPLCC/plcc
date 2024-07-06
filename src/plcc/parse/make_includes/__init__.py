from itertools import flatten
from functools import partial


from .include import Include


def resolve_includes(lines, read_fn=None):
    if read_fn is None:
        read_fn = lambda filePath: \
                mark_includes(mark_blocks(to_lines(split_lines(read(filePath)))))

    def _resolve(o):
        if not isinstance(o, Include):
            return [o]
        filePath = Path(o.file)
        if not filePath.is_absolute():
            sp = Path(o.line.file)
            filePath = (sp.parent/filePath).resolve()
        return resolve_includes(read_fn(filePath))

    return list(flatten(map(_resolve, lines)))


def mark_includes(lines):
    def to_include(thing):
        if not isinstance(thing, Line):
            return thing
        m = re.match(r'^include (?P<file>[^\0]$', thing.string)
        if m:
            return Include(m['file'])
        else:
            return thing
    return list(map(to_include, lines))


def mark_blocks():
#YICK YICK YICK
    open_patterns = {
        re.compile(r'^%%%(\s*#.*)?$'): ppp,
        re.compile(r'^%%{(\s*#.*)?$'): ppl,
    }

    seeking_close = None

    def scan(pattern_callbacks, lines):
        for line in lines:
            for k in pattern_callbacks:
                m = k.match(line.string)
                if m:
                    pattern_callbacks[k](line)

    def ppp(line):
        ...

    def ppl():
        open_block(line)

    def ppr(line):
        close_block(line)
        ...

    scan({
        re.compile(r'^%%%(\s*#.*)?$'): ppp,
        re.compile(r'^%%{(\s*#.*)?$'): ppl,
        re.compile(r'^%%}(\s*#.*)?$'): ppr,
    })


def to_lines(stringList, start, file):
    return [Line(s, i, file) for i, s in enumerate(stringList, start=start)]


def split_lines(string):
    return string.splitlines()


def read(filePath):
    with Path(filePath).open('r') as f:
        return f.read()
