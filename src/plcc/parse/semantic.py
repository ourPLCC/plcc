
class SemanticParser:

    def parse(self, lines):
        ...


def sem(nxt, stubs, semFlag, destFlag, fileExt):
    global argv
    # print('=== semantic routines')
    if not getFlag(semFlag):
        stubs = stubs.getStubs()
        semFinishUp(stubs, destFlag, fileExt)
        done()
    for line in nxt:
        line = line.strip()
        if line == "%":
            break
        if len(line) == 0 or line[0] == '#':
            # skip comments or blank lines
            continue
        (cls, _, mod) = line.partition(':')
        # print('>>> cls={} mod={}'.format(cls, mod))
        cls = cls.strip()
        codeString = getCode(nxt) # grab the stuff between %%% ... %%%
        if line[-8:] == ':ignore!':
            continue
        # check to see if line has the form Class:mod
        mod = mod.strip() # mod might be 'import', 'top', etc.
        try:
            stubs.addCodeToClass(cls, mod, codeString)
        except StubDoesNotExistForHookException as e:
            deathLNO(str(e))


    stubs = stubs.getStubs()
    semFinishUp(stubs, destFlag, fileExt)

def getCode(nxt):
    code = []
    offset = None
    for line in nxt:
        line = line.rstrip()
        if re.match(r'\s*#', line) or re.match(r'\s*$', line):
            # skip comments or blank lines
            continue
        if re.match(r'%%{', line): # legacy plcc
            stopMatch = r'%%}'
            break
        if re.match(r'%%%', line):
            stopMatch = r'%%%'
            break
        else:
            deathLNO('expecting a code segment')
    lineMode = True # switch on line mode
    for line in nxt:
        if re.match(stopMatch, line):
            break
        if offset == None:
            offset = getOffset(line)
        line = removeOffset(line, offset)
        code.append(line)
    else:
        deathLNO('premature end of file')
    lineMode = False # switch off line mode
    if len(code)>0 :
        while len(code[0]) == 0:
            code.pop(0)
        while len(code[-1]) == 0:
            code.pop()
    return code
