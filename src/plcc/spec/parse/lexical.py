import re

from .error import ParseError
from .spec import LexicalSpec


def parseLexicalSpec(sectionLines):
    termSpecs = parse(sectionLines)
    return LexicalSpec(termSpecs)


def parse(sectionLines):
    '''
    A token that has a substring like this ' #' will mistakenly be
    considered as a comment. Use '[ ]#' instead.
    '''
    shouldProcessPatterns = True
    term = set()
    termSpecs = []

    # Handle any flags appearing at beginning of lexical spec section;
    # turn off when all flags have been processed
    flagSwitch = True # turn off after all the flags have been processed
    for line_obj in lines:
        line = line_obj.text
        line = re.sub(r'\s+#.*', '', line)   # remove trailing comments ...
        line = line.strip()
        if len(line) == 0: # skip empty lines
            continue
        if line[0] == '#': # skip comments
            continue
        if line[0] == '!': # handle a PLCC compile-time flag
            if flagSwitch:
                line = line[1:]
                try:
                    processFlag(line)
                except Exception as msg:
                    raise ParseError(line_obj, str(msg))
                continue
            else:
                raise ParseError(
                    line_obj,
                    'all PLCC flags must occur before token/skip specs'
                )
        flagSwitch = False # stop accepting compile-time flags
        jpat = '' # the Java regular expression pattern for this skip/term
        if shouldProcessPatterns:
            # handle capturing the match part and replacing with empty string
            def qsub(match):
                nonlocal jpat
                if match:
                    jpat = match.group(1)
                return ''
            pat = r"\s'(.*)'$"
            line = re.sub(pat, qsub, line)
            if jpat:
                # add escapes to make jpat into a Java string
                jpat = re.sub(r'\\', r'\\\\', jpat)
                jpat = re.sub('"', r'\\"', jpat)
            else:
                pat = r'\s"(.*)"$'
                line = re.sub(pat, qsub, line)
                if not jpat:
                    raise ParseError(line_obj, 'No legal pattern found!')
            jpat = '"' + jpat + '"'  # quotify
            # make sure there are no spurious single
            # or double quotes remaining in line
            if re.search("[\"']", line):
                raise ParseError(line_obj, 'Puzzling skip/token pattern specification.')
        # next determine if it's a skip or token specification
        result = line.split()
        rlen = len(result)
        if rlen >= 3:
            raise ParseError(line_obj, 'Illegal skip/token specification')
        if rlen == 0:
            raise ParseError(line_obj, 'No skip/token symbol')
        if rlen == 1:
            result = ['token'] + result # defaults to a token
        what = result[0]  # 'skip' or 'token'
        name = result[1]  # the term/skip name
        if not isTerm(name):
            raise ParseError(line_obj, f'{name}: illegal token name')
        if name in term:
            raise ParseError(line_obj, f'{name}: duplicate token/skip name')
        term.update({name})
        if what == 'skip':
            skip = ', TokType.SKIP'   # Java constant
        elif what == 'token':
            skip = ''
        else:
            raise ParseError(line_obj, 'No skip/token specification found')
        if shouldProcessPatterns:
            push(termSpecs, '{} ({}{})'.format(name, jpat, skip))
        else:
            termSpecs.append(name)
    return termSpecs
