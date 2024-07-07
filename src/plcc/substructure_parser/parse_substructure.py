from .parse_lines import parse_lines
from .parse_blocks import parse_blocks
from .parse_dividers import parse_dividers
from .parse_includes import parse_includes
from .process_includes import process_includes, parse_file

def parse_substructure(string,
        process_includes=process_includes,
        parse_includes=parse_includes,
        parse_blocks=parse_blocks,
        parse_dividers=parse_dividers,
        parse_lines=parse_lines):
    if string is None:
        return
    return process_includes(parse_file=parse_file,
        lines=parse_dividers(
            parse_includes(
                parse_blocks(
                    parse_lines(
                        string
                    )
                )
            )
        )
    )
