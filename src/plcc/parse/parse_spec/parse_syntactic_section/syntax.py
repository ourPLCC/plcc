import re

# tokens

COMMENT=r'\s*#.*'
TERMINAL=r'\s*(?P<terminal>[A-Z_][A-Z0-9_]*)\s*'
NONTERMINAL=r'\s*(?P<nonterminal>[a-z_]\w*)\s*'
DISAMBIGUATION=r'\s*:?\s*(?P<disambiguation>\w+)\s*'
REPEATING_OP=r'\s*\*\*=\s*'
STANDARD_OP=r'\s*::=\s*'
LA=r'\s*<\s*'
RA=r'\s*>\s*'
PLUS=r'\s*\+\s*'


# high-level tokens

def opt(regex):
    return '(?:' + regex + ')?'

start_repeating_rule = re.compile(LA + NONTERMINAL + RA + opt(DISAMBIGUATION) + REPEATING_OP)
start_standard_rule = re.compile(LA + NONTERMINAL + RA + opt(DISAMBIGUATION) + STANDARD_OP)
terminal = re.compile(TERMINAL)
capturing_terminal = re.compile(LA + TERMINAL + RA + opt(DISAMBIGUATION))
nonterminal = re.compile(LA + NONTERMINAL + RA + opt(DISAMBIGUATION))
separator = re.compile(PLUS + TERMINAL)
