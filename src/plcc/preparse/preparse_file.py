import re


from .read_file import read_file
from .parse_lines import parse_lines, Line
from .parse_blocks import parse_blocks, Block, UnclosedBlockError
from .parse_includes import parse_includes, Include
from .process_includes import process_includes, CircularIncludeError


from pathlib import Path


def preparse_file(file):

    PPP = re.compile(r'^%%%(?:\s*#.*)?$')
    PPLC = re.compile(r'^%%{(?:\s*#.*)?$')
    PPRC = re.compile(r'^%%}(?:\s*#.*)?$')
    INCLUDE=r'^%include\s+(?P<file>[^\0]+)$'

    BLOCK_BRACKETS= {
        PPP: PPP,
        PPLC: PPRC
    }

    def parse_file(file):
        file = str(Path(file).resolve())
        string = read_file(file)
        lines = parse_lines(string, start=1, file=file, Line=Line)
        blocks_and_lines = parse_blocks(lines, brackets=BLOCK_BRACKETS, Block=Block)
        includes_blocks_and_lines = parse_includes(blocks_and_lines, pattern=INCLUDE, Include=Include)
        return includes_blocks_and_lines

    return process_includes(parse_file(file), parse_file=parse_file)
