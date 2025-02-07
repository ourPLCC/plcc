# -*-python-*-

"""
    PLCC: A Programming Languages Compiler-Compiler
    Copyright (C) 2023  Timothy Fossum <plcc@pithon.net>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sys
import re
import os
import pathlib
import io
import shutil
import tempfile

from plcc.java import spec as java_spec
from plcc.python import spec as python_spec

argv = sys.argv[1:] # skip over the command-line argument


# current file information
Fname = ''          # current file name (STDIN if standard input)
Lno = 0             # current line number in file
Line = ''           # current line in the file
nlgen = None        # next line generator for Fname
STD = []            # reserved names from Std library classes
STDT = []           # token-related files in the Std library directory
STDP = []           # parse/runtime-related files in the Std library directory

flags = {}          # processing flags (dictionary)

lineMode = False    # True if in line mode

startSymbol = ''    # start symbol (first nonterm in rules)
term = set()        # set of term (token) names
termSpecs = []      # term (token) specifications for generating the Token file

nonterms = set()    # set of all nonterms
fields = {}         # maps a non-abstract class name to its list of fields
rules = []          # list of items  of the form (nt, cls, rhs),
                    # one for each grammar rule
extends = {}        # maps a derived class to its abstract base class
derives = {}        # maps an abstract class to a list of its derived classes
cases = {}          # maps a non-abstract class to its set of case terminals
                    # for use in a switch
rrule = {}          # maps a repeating rule class name to its separator string
                    # (or None)
stubs = {}          # maps a class name to its parser stub file
python_stubs = {}

def debug(msg, level=1):
    # print(getFlag('debug'))
    if msg and getFlag('debug') >= level:
        print('%%% {}'.format(msg), file=sys.stderr)
        return True
    return False

def debug2(msg):
    debug(msg, level=2)

def LIBPLCC():
    return str(pathlib.Path(__file__).parent)

def main():
    global argv
    plccInit()
    while argv:
        if argv[0] == '--':
            # just continue with the rest of the command line
            argv = argv[1:]
            break
        (flag, ee, val) = argv[0].partition("=")
        # print('>>> flag={} val={}'.format(flag, val))
        flag = flag.strip()
        if  flag[:2] == '--':
            key = flag[2:].strip()
            if key == '':
                # no key
                death('illegal command line parameter')
            val = val.strip()
            if ee:
                # map key to val, using processFlag
                try:
                    processFlag('{}={}'.format(key, val))
                except Exception as msg:
                    death(msg)
            else:
                processFlag(key)
            argv = argv[1:]
        else:
            break

    # Handle --version option.
    if 'version' in flags and flags['version']:
        import plcc.version
        print(plcc.version.get_version())
        sys.exit(0)

    jsonAstInit()

    nxt = nextLine()     # nxt is the next line generator
    lex(nxt)    # lexical analyzer generation
    par(nxt)    # LL(1) check and parser generation
    sem(nxt, stubs, **java_spec)
    # sem(nxt, python_stubs, **python_spec)
    done()

def plccInit():
    global flags, argv, STD, STDT, STDP
    STDT = ['ILazy','IMatch','IScan','ITrace', 'Trace', 'PLCCException', 'Scan']
    STDP = ['ProcessFiles','Parse','Rep']
    STD = STDT + STDP
    STD.append('Token')
    # file-related flags -- can be overwritten
    # by a grammar file '!flag=...' spec
    # or by a '--flag=...' command line argument
    for fname in STD:
        flags[fname] = fname
    flags['libplcc'] = LIBPLCC()
    flags['Token'] = True         # generate scanner-related files
    # behavior-related flags
    flags['debug'] = 0                  # default debug value
    flags['destdir'] = 'Java'           # the default destination directory
    flags['python_destdir'] = 'Python'  # default destination for fourth section semantics (Python)
    flags['pattern'] = True             # create a scanner that uses re. patterns
    flags['LL1'] = True                 # check for LL(1)
    flags['parser'] = True              # create a parser
    flags['semantics'] = True           # create java semantics routines
    flags['python_semantics'] = True    # create python semantics routines
    flags['nowrite'] = False            # when True, produce *no* file output

def jsonAstInit():
    global flags, STD, STDP
    if 'json_ast' in flags and flags['json_ast']:
        if 'ParseJsonAst' not in STDP:
            if 'ParseJsonAst' not in STD:
                STDP.append('ParseJsonAst')
                flags['ParseJsonAst'] = 'ParseJsonAst'

def lex(nxt):
    # print('=== lexical specification')
    # Handle any flags appearing at beginning of lexical spec section;
    # turn off when all flags have been processed
    flagSwitch = True # turn off after all the flags have been processed
    for line in nxt:
        line = re.sub(r'\s+#.*', '', line)   # remove trailing comments ...
        # NOTE: a token that has a substring like this ' #' will mistakenly be
        # considered as a comment. Use '[ ]#' instead
        line = line.strip()
        if len(line) == 0: # skip empty lines
            continue
        if line[0] == '#': # skip comments
            continue
        if line[0] == '!': # handle a PLCC compile-time flag
            if flagSwitch:
                line = line[1:]
                # print ('>>> flag line: {}'.format(line))
                try:
                    processFlag(line)
                except Exception as msg:
                    deathLNO(msg)
                continue
            else:
                deathLNO('all PLCC flags must occur before token/skip specs')
        flagSwitch = False # stop accepting compile-time flags
        if line == '%':
            break; # end of lexical specification section
        # print ('>>> {}'.format(line))
        jpat = '' # the Java regular expression pattern for this skip/term
        pFlag = getFlag('pattern')
        # only process patterns if the 'pattern' flag is True
        if pFlag:
            # handle capturing the match part and replacing with empty string
            def qsub(match):
                nonlocal jpat
                if match:
                    jpat = match.group(1)
                    # print('>>> match found: jpat={}'.format(jpat))
                return ''
            pat = r"\s'(.*)'$"
            # print('>>> q1 pat={}'.format(pat))
            line = re.sub(pat, qsub, line)
            if jpat:
                # add escapes to make jpat into a Java string
                jpat = re.sub(r'\\', r'\\\\', jpat)
                jpat = re.sub('"', r'\\"', jpat)
                # print('>>> q1 match found: line={} jpat={}'.format(line,jpat))
                pass
            else:
                pat = r'\s"(.*)"$'
                # print('>>> q2 pat={}'.format(pat))
                line = re.sub(pat, qsub, line)
                if jpat:
                    # print('>>> q2 match found: line={} jpat={}'.format(line,jpat))
                    pass
                else:
                    deathLNO('No legal pattern found!')
            jpat = '"' + jpat + '"'  # quotify
            # print('>>> line={} jpat={}'.format(line,jpat))
            # make sure there are no spurious single
            # or double quotes remaining in line
            if re.search("[\"']", line):
                deathLNO('Puzzling skip/token pattern specification')
        # next determine if it's a skip or token specification
        result = line.split()
        rlen = len(result)
        if rlen >= 3:
            deathLNO('Illegal skip/token specification')
        if rlen == 0:
            deathLNO('No skip/token symbol')
        if rlen == 1:
            result = ['token'] + result # defaults to a token
        what = result[0]  # 'skip' or 'token'
        name = result[1]  # the term/skip name
        if not isTerm(name):
            deathLNO(name + ': illegal token name')
        if name in term:
            deathLNO(name + ': duplicate token/skip name')
        term.update({name})
        if what == 'skip':
            skip = ', TokType.SKIP'   # Java constant
        elif what == 'token':
            skip = ''
        else:
            deathLNO('No skip/token specification found')
        if pFlag:
            push(termSpecs, '{} ({}{})'.format(name, jpat, skip))
        else:
            push(termSpecs, name)
    lexFinishUp()

def lexFinishUp():
    global termSpecs, STDT
    if len(termSpecs) == 0:
        death('No tokens specified -- quitting')
    # first create the destination (Java) directory if necessary
    if getFlag('nowrite'):
        # don't write any files
        return
    dst = getFlag('destdir')
    if not dst:
        death('illegal destdir flag value')
    try:
        os.mkdir(str(dst))
        debug('[lexFinishUp] ' + dst + ': destination subdirectory created')
    except FileExistsError:
        debug('[lexFinishUp] ' + dst + ': destination subdirectory exists')
    except:
        death(dst + ': error creating destination subdirectory')

    if not getFlag('Token'):
        return # do not create any automatically generated scanner-related files
    libplcc = getFlag('libplcc')
    std = pathlib.Path(libplcc) / 'lib' / 'Std'
    try:
        os.mkdir(str(std))
    except FileExistsError:
        pass
    except:
        death(str(std) + ': cannot access directory')
    fname = '{}/{}'.format(dst, 'Token.java')
    try:
        tokenFile = open(fname, 'w')
    except:
        death('Cannot open ' + fname + ' for writing')
    if getFlag('pattern'):
        # use the Token.pattern library file to create Token.java
        fname = 'Token.pattern'
        try:
            tokenTemplate = open('{}/{}'.format(std, fname))
        except:
            death(fname + ': cannot read library file')
        for line in tokenTemplate:
            # note that line keeps its trailing newline
            if re.match('^%%Match%%', line):
                for ts in termSpecs:
                    print('        ' + ts + ',', file=tokenFile)
            else:
                print(line, file=tokenFile, end='')
        tokenTemplate.close()
    else:
        # use the Token.template file to create Token.java
        fname = 'Token.template'
        try:
            tokenTemplate = open('{}/{}'.format(std, fname))
        except:
            death(fname + ': cannot read library file')
        for line in tokenTemplate:
            # note that line keeps its trailing newline
            if re.match('^%%Match%%', line):
                tssep = ''
                for ts in termSpecs:
                    print(tssep + '        ' + ts, file=tokenFile, end='')
                    tssep = ',\n'
                print(';', file=tokenFile)
            else:
                print(line, file=tokenFile, end='')
        tokenTemplate.close()
    tokenFile.close()
    # copy the Std token-related library files to the destination directory
    for fname in STDT:
        if getFlag(fname):
            debug('[lexFinishUp] copying {} from {} to {} ...'.format(fname, std, dst))
            try:
                shutil.copy('{}/{}.java'.format(std, fname), '{}/{}.java'.format(dst, fname))
            except:
                death('Failure copying {} from {} to {}'.format(fname, std, dst))

def par(nxt):
    debug('[par] processing grammar rule lines')
    if not getFlag('parser'):
        done()
    rno = 0
    for line in nxt:
        line = re.sub('#.*$', '', line) # remove comments
        line = line.strip()
        if len(line) == 0:
            continue                    # skip entirely blank lines
        if line == '%':
            break
        rno += 1
        processRule(line, rno)
    parFinishUp()


def parFinishUp():
    global STDP, startSymbol, nonterms, extends, derives, rules
    if not rules:
        print('No grammar rules')
        return
    debug('[parFinishUp] par: finishing up...')
    # check to make sure all RHS nonterms appear as the LHS of at least one rule
    for nt in nonterms:
        debug('[parFinishUp] nt={}'.format(nt))
    for (nt, cls, rhs) in rules:
        rhsString = ''
        for item in rhs:
            debug('[parFinishUp] item={}'.format(item))
            if isNonterm(item):
                rhsString += ' <{}>'.format(item)
                if not item in nonterms:
                    death('nonterm {} appears on the RHS of rule "<{}> ::= {} ..." but not on any LHS'.format(item, nt, rhsString))
            else:
                rhsString += ' {}'.format(item)
        debug('[parFinishUp] rule: "<{}> ::= {}"'.format(nt, rhsString))
    # if debugging, print all of the extends and derives items
    for cls in extends:
        debug('[parFinishUp] class {} extends {}'.format(cls, extends[cls]))
    for base in derives:
        debug('[parFinishUp] base class {} derives {}'.format(base, derives[base]))
    # print the nonterminals
    print('Nonterminals (* indicates start symbol):')
    for nt in sorted(nonterms):
        if nt[-1] == '#':
            continue  # ignore automatically generated repeating rule names
        if nt == startSymbol:
            ss = ' *<{}>'.format(nt)
        else:
            ss = '  <{}>'.format(nt)
        print(ss)
    print()

    # print abstract classes
    print('Abstract classes:')
    for cls in sorted(derives):
        print('  {}'.format(cls))

    # check for LL1
    if getFlag('LL1'):
        checkLL1()

    if getFlag('nowrite'):
        return
    # copy the Std parser-related files
    dst = getFlag('destdir')
    libplcc = getFlag('libplcc')
    std = pathlib.Path(libplcc) / 'lib' / 'Std'
    for fname in STDP:
        if getFlag(fname):
            debug('[parFinishUp] copying {} from {} to {} ...'.format(fname, std, dst))
            try:
                shutil.copy('{}/{}.java'.format(std, fname), '{}/{}.java'.format(dst, fname))
            except:
                death('Failure copying {} from {} to {}'.format(fname, std, dst))

    # build parser stub classes
    buildStubs(stubs, **java_spec)
    buildStubs(python_stubs, **python_spec)
    # build the _Start.java file from the start symbol
    buildStart()

def processRule(line, rno):
    global STD, startSymbol, fields, rules, rrule, nonterm, extends, derives
    if rno:
        debug('[processRule] rule {:3}: {}'.format(rno, line))
    tnt = line.split()     # LHS ruleType RHS
    if len(tnt) < 2:
        deathLNO('illegal grammar rule') # no ruleType
    lhs = tnt.pop(0)       # the LHS of this rule
    nt, cls = defangLHS(lhs)
    base = nt2cls(nt)      # the base (class) name of this nonterminal
    if base == cls:
        deathLNO('base class and derived class names cannot be the same!')
    if base in STD:
        deathLNO('{}: reserved class name'.format(base))
    if cls != None and cls in STD:
        deathLNO('{}: reserved class name'.format(cls))
    ruleType = tnt.pop(0)  # either '**=' or '::='
    rhs = tnt              # a list of all the items to the right
                           # of the ::= or **= on the line
    if ruleType == '**=':  # this is a repeating rule
        if cls != None:
            deathLNO('repeating rule cannot specify a non base class name')
        if startSymbol == '':
            deathLNO('repeating rule cannot be the first grammar rule')
        if len(rhs) == 0:
            deathLNO('repeating rules cannot be empty')
        debug('[processRule] repeating rule: ' + line)
        sep = rhs[-1] # get the last entry in the line
        if sep[0] == '+':
            # must be a separated list
            sep = sep[1:]   # remove the leading '+' from the separator
            if not isTerm(sep):
                deathLNO('separator '+sep+' in repeating rule must be a bare Token')
            rhs.pop()       # remove separator from the rhs list
        else:
            sep = None
        # a repeating rule has no derived classes, so it's just a base class
        # saveFields(base, lhs, rhs) ?? check for duplicate classes,
        # then map the base to its (lhs, rhs) pair
        rrule[base] = sep   # mark base as a repeating rule class with separator sep
                            # (possibly None)
        # next add right-recursive rules to the rule set to simulate repeating rules
        rhsString = ' '.join(rhs)
        if sep:
            ntsep = nt+'#'  # 'normal' nonterms cannot have '#' symbols
            processRule('<{}>      ::= {} <{}>'.format(nt, rhsString, ntsep), None)
            processRule('<{}>:void ::='.format(nt), None)
            processRule('<{}>:void ::= {} {} <{}>'.format(ntsep, sep, rhsString, ntsep), None)
            processRule('<{}>:void ::='.format(ntsep), None)
        else:
            processRule('<{}>      ::= {} <{}>'.format(nt, rhsString, nt), None)
            processRule('<{}>:void ::='.format(nt), None)
        return
    elif not ruleType == '::=':
        deathLNO('illegal grammar rule syntax')
    # at this point, we may have a legal non-repeating rule
    debug('[processRule] so far: {} ::= {}'.format(lhs, rhs))
    nonterms.update({nt}) # add nt to the set of LHS nonterms
    if cls == 'void':
        # this rule is *generated* by a repeating rule,
        # so there are no further class-related actions to do
        saveRule(nt, lhs, None, rhs)
        return
    if startSymbol == '':
        startSymbol = nt   # the first lhs nonterm is the start symbol
    if cls == None:
        # a simple base class -- no derived classes involved
        saveRule(nt, lhs, base, rhs)
        return
    # if we get here, cls (non-abstract) is a new class derived from base (abstract)
    if cls in derives:
        deathLNO('non-abstract class {} is already defined as an abstract class'.format(cls))
    if base in fields:
        deathLNO('abstract base class {} already exists as a non-abstract class'.format(base))
    saveRule(nt, lhs, cls, rhs)
    extends[cls] = base
    if base in derives:
        derives[base].update({cls})
    else:
        derives[base] = {cls}

def saveRule(nt, lhs, cls, rhs):
    """ construct a tuple of the form (nt, tnts) where nt is the LHS nonterm
        (minus the <>) and tnts is a list of the terminal/nonterm items
        extracted from the rhs (and excluding their field names).
        Then add this to the rules list for determining LL1.
        Also, map fields[cls] to the (lhs, rhs) pair
    """
    global rules, fields, rrule
    if cls != None:
        if cls in fields:
            deathLNO('class {} is already defined'.format(cls))
        if cls in rrule:
            fields[cls] = (lhs, rhs[:-1]) # remove the separator token
        else:
            fields[cls] = (lhs, rhs)
    tnts = []
    for item in rhs:
        tnt, field = defangRHS(item)
        if tnt == None: # item is a bare token
            tnt = item;
        tnts.append(tnt) # tnt may be a nonterm or a token name
    rules.append((nt, cls, tnts)) # add the rule tuple to the rules list

def checkLL1():
    global rules, nonterms, cases
    first = {}
    follow = {}
    switch = {}

    def getFirst(form):
        nonlocal first
        # return the first set (of terminals) of this sentential form
        fst = set()
        if len(form) == 0:         # the form is empty, so it only derives Null
            return {'Null'}
        tnt = form[0]              # get the item at the start of the sentential form
        if isTerm(tnt):
            return {tnt}           # the form starts with a terminal, which is clearly its only first set item
        # tnt must be a nonterm -- get the first set for this and add it to our current set
        f = first[tnt]             # get the current first set for tnt (=form[0])
        for t in f:
            # add all non-null stuff from first[tnt] to the current first set
            if t != 'Null':
                fst.update({t})
            else:
                # Null is in the first set for f, so recursively add the nonterms from getFirst(form[1:])
                fst.update(getFirst(form[1:]))
        # debug('first set for {}: {}'.format(form, fst))
        return fst

    for nt in nonterms:
        first[nt] = set()        # initialize all of the first sets
        follow[nt] = set()       # initialize all of the follow sets
        switch[nt] = []          # maps each nonterm to a list of its first sets

    # determine the first sets
    modified = True
    while modified:
        modified = False  # assume innocent
        for (nt, cls, rhs) in rules:
            fst = first[nt]      # the current first set for this nonterminal
            fct = len(fst)       # see if the first set changes
            fst.update(getFirst(rhs))   # add any new terminals to the set
            if len(fst) != fct:
                modified = True
    if debug('[checkLL1] First sets:'):
        for nt in nonterms:
            debug('[checkLL1] {} -> {}'.format(nt, first[nt]))

    # determine the follow sets
    modified = True
    while modified:
        modified = False
        for (nt, cls, rhs) in rules:
            rhs = rhs[:]         # make a copy
            debug('[checkLL1] examining rule {} ::= {}'.format(nt, ' '.join(rhs)))
            while rhs:
                tnt = rhs.pop(0) # remove the first element of the list
                if isNonterm(tnt):
                    # only nonterminals count for determining follow sets
                    fol = follow[tnt]              # the current follow set for tnt
                    fct = len(fol)
                    for t in getFirst(rhs):        # look at the first set of what follows tnt (the current rhs)
                        if t == 'Null':
                            fol.update(follow[nt]) # if the rhs derives the empty string, what follows nt must follow tnt
                        else:
                            fol.update({t})        # otherwise, what the rhs derives must follow tnt
                    if len(fol) != fct:
                        modified = True
    if debug('[checkLL1] Follow sets:'):
        for nt in nonterms:
            debug('[checkLL1]   {}: {}'.format(nt, ' '.join(follow[nt])))

    # determine the switch sets for each nonterm and corresponding rhs
    for (nt, cls, rhs) in rules:
        # print('### nt={} cls={} rhs= {}'.format(nt, cls, ' '.join(rhs)))
        fst = getFirst(rhs)
        if 'Null' in fst:
            # the rhs can derive the empty string, so remove Null from the set
            fst -= {'Null'}
            # add all of the terminals in follow[nt] to this switch set
            fst.update(follow[nt])
        switch[nt].append((fst, rhs))
        if cls != None:
            saveCases(cls, fst)
    if debug('[checkLL1] nonterm switch sets:'):
        for nt in switch:
            debug('[checkLL1] {} => {}'.format(nt, switch[nt]))

    # finally check for LL(1)
    for nt in switch:
        allTerms = set()
        for (fst, rhs) in switch[nt]:
            debug('[checkLL1] nt={} fst={} rhs={}'.format(nt, fst, rhs))
            s = allTerms & fst   # check to see if fst has any tokens already in allTerms
            if s:
                death('''\
not LL(1):
term(s) {} appears in first sets for more than one rule starting with nonterm {}
'''.format(' '.join(fst), nt))
            else:
                allTerms.update(fst)
        if not allTerms:
            death('possibly useless or left-recursive grammar rule for nonterm {}'.format(nt))
        cases[nt] = allTerms
    pass

def saveCases(cls, fst):
    global cases, derives
    if cls in cases:
        death('cases for class {} already accounted for'.format(cls))
    if cls in derives:
        death('{} is an abstract class'.format(cls))
    # print('### class={} cases={}'.format(cls, ' '.join(fst)))
    cases[cls] = fst

def buildStubs(
        stubs,
        abstractStubFormatString,
        stubFormatString,
        extendFormatString,
        declFormatString,
        initFormatString,
        paramFormatString,
        **ignored_kwargs):
    global fields, derives
    for cls in derives:
        # make parser stubs for all abstract classes
        if cls in stubs:
            death('duplicate stub for abstract class {}'.format(cls))
        debug('[buildStubs] making stub for abstract class {}'.format(cls))
        stubs[cls] = makeAbstractStub(cls, abstractStubFormatString,
            ext=' extends _Start',
            caseIndentLevel=2)
    for cls in fields:
        # make parser stubs for all non-abstract classes
        if cls in stubs:
            death('duplicate stub for class {}'.format(cls))
        debug('[buildStubs] making stub for non-abstract class {}'.format(cls))
        stubs[cls] = makeStub(cls, stubFormatString,
            extendFormatString,
            declFormatString,
            initFormatString,
            paramFormatString)


def makeAbstractStub(
        base,
        formatString,
        ext=' extends _Start',
        caseIndentLevel=2):
    global cases
    caseList = []    # a list of strings,
                     # either 'case XXX:'
                     # or '    return Cls.parse(...);'
    for cls in derives[base]:
        if len(cases[cls]) == 0:
            death('class {} is unreachable'.format(cls))
        for tok in cases[cls]:
            caseList.append('case {}:'.format(tok))
        caseList.append('    return {}.parse(scn$,trace$);'.format(cls))
    if base != nt2cls(startSymbol):
        ext = ''
    stubString = formatString.format(cls=cls,
           base=base,
           ext=ext,
           cases='\n'.join(indent(caseIndentLevel, caseList))
          )
    return stubString

def makeStub(cls, formatString, extendFormatString, declFormatString,
        initFormatString, paramFormatString):
    global fields, extends, rrule
    # make a stub for the given non-abstract class
    debug('[makeStub] making stub for non-abstract class {}'.format(cls))
    sep = False
    (lhs, rhs) = fields[cls]
    ext = '' # assume not an extended class
    # two cases: either cls is a repeating rule, or it isn't
    if cls in rrule:
        ruleType = '**='
        sep = rrule[cls]
        (fieldVars, parseString) = makeArbnoParse(cls, rhs, sep)
        if sep != None:
            rhs = rhs + ['+{}'.format(sep)]
    else:
        ruleType = '::='
        (fieldVars, parseString) = makeParse(cls, rhs)
        # two sub-cases: either cls is an extended class (with abstract base class) or it's a base class
        if cls in extends:
            ext = extendFormatString.format(cls=extends[cls])
    ruleString = '{} {} {}'.format(lhs, ruleType, ' '.join(rhs))
    # fieldVars = makeVars(cls, rhs)
    decls = []
    inits = []
    params = []
    for (field, fieldType) in fieldVars:
        decls.append(declFormatString.format(fieldType=fieldType, field=field))
        inits.append(initFormatString.format(field=field))
        params.append(paramFormatString.format(fieldType=fieldType, field=field))
    debug('[makeStub] cls={} decls={} params={} inits={}'.format(cls, decls, params, inits))
    debug('[makeStub] rule: {}'.format(ruleString))
    if cls == nt2cls(startSymbol):
        ext = extendFormatString.format(cls='_Start')
    stubString = formatString.format(cls=cls,
           lhs=lhs,
           ext=ext,
           ruleString=ruleString,
           decls='\n'.join(indent(1,decls)),
           params=', '.join(params),
           inits='\n'.join(indent(2,inits)),
           parse=parseString)
    return stubString

def indent(n, iList):
    ### make a new list with the old list items prepended with 4*n spaces
    indentString = '    '*n
    newList = []
    for item in iList:
        newList.append('{}{}'.format(indentString, item))
    # print('### str={}'.format(str))
    return newList

def makeParse(cls, rhs):
    args = []
    parseList = []
    fieldVars = []
    fieldSet = set()
    rhsString = ' '.join(rhs)
    for item in rhs:
        (tnt, field) = defangRHS(item)
        if tnt == None:
            # item must be a bare token -- just match it
            parseList.append('scn$.match(Token.Match.{}, trace$);'.format(item))
            continue
        if field in fieldSet:
            deathLNO('duplicate field name {} in rule RHS {}'.format(field, rhsString))
        fieldSet.update({field})
        args.append(field)
        if isTerm(tnt):
            fieldType = 'Token'
            parseList.append(
                'Token {} = scn$.match(Token.Match.{}, trace$);'.format(field, tnt))
        else:
            fieldType = nt2cls(tnt)
            parseList.append(
                '{} {} = {}.parse(scn$, trace$);'.format(fieldType, field, fieldType))
        fieldVars.append((field, fieldType))
    parseList.append('return new {}({});'.format(cls, ', '.join(args)))
    debug('[makeParse] parseList={}'.format(parseList))
    parseString = '\n'.join(indent(2, parseList))
    return (fieldVars, parseString)

def makeArbnoParse(cls, rhs, sep):
    # print('%%%%%% cls={} rhs="{}" sep={}'.format(cls, ' '.join(rhs), sep))
    global cases
    inits = []       # initializes the List fields
    args = []        # the arguments to pass to the constructor
    loopList = []    # the match/parse code in the Arbno loop
    fieldVars = []   # the field variable names (all Lists), to be returned
    fieldSet = set() # the set of field variable names for this RHS
    rhsString = ' '.join(rhs)
    # rhs = rhs[:-1]   # remove the last item from the grammar rule (which has an underscore item)
    # create the parse statements to be included in the loop
    switchCases = [] # the token cases in the switch statement
    for item in rhs:
        (tnt, field) = defangRHS(item)
        if tnt == None:
            loopList.append('scn$.match(Token.Match.{}, trace$);'.format(item))
            continue
        # field is either derived from tnt or is an annotated field name
        field += 'List'
        if isTerm(tnt):
            # a token
            baseType = 'Token'
            loopList.append(
                '{}.add(scn$.match(Token.Match.{}, trace$));'.format(field, tnt))
        elif isNonterm(tnt):
            baseType = nt2cls(tnt)
            loopList.append('{}.add({}.parse(scn$, trace$));'.format(field, baseType))
        else:
            pass # cannot get here
        args.append(field)
        if field in fieldSet:
            deathLNO(
                'duplicate field name {} in RHS rule {}'.format(field, rhsString))
        fieldSet.update({field})
        fieldType = 'List<{}>'.format(baseType)
        fieldVars.append((field, fieldType))
        inits.append('{} {} = new ArrayList<{}>();'.format(fieldType, field, baseType))
    switchCases = []
    if len(cases[cls]) == 0:
        deathLNO('class {} is unreachable'.format(cls))
    for item in cases[cls]:
        switchCases.append('case {}:'.format(item))
    returnItem = 'return new {}({});'.format(cls, ', '.join(args))
    if sep == None:
        # no separator
        parseString = """\
{inits}
        while (true) {{
            Token t$ = scn$.cur();
            Token.Match match$ = t$.match;
            switch(match$) {{
{switchCases}
{loopList}
                continue;
            default:
                {returnItem}
            }}
        }}
""".format(inits='\n'.join(indent(2, inits)),
           switchCases='\n'.join(indent(3, switchCases)),
           loopList='\n'.join(indent(4, loopList)),
           returnItem=returnItem)
    else:
        # there's a separator
        parseString = """\
{inits}
        // first trip through the parse
        Token t$ = scn$.cur();
        Token.Match match$ = t$.match;
        switch(match$) {{
{switchCases}
            while(true) {{
{loopList}
                t$ = scn$.cur();
                match$ = t$.match;
                if (match$ != Token.Match.{sep})
                    break; // not a separator, so we're done
                scn$.match(match$, trace$);
            }}
        }} // end of switch
        {returnItem}
""".format(inits='\n'.join(indent(2, inits)),
           switchCases='\n'.join(indent(2, switchCases)),
           loopList='\n'.join(indent(4, loopList)),
           returnItem=returnItem,
           sep=sep)
    debug('[makeArbnoParse] fieldVars={}'.format(fieldVars))
    return (fieldVars, parseString)

def buildStart():
    global startSymbol
    # build the _Start.java file
    if startSymbol == '':
        death('no start symbol!')
    dst = getFlag('destdir')
    if dst == None or getFlag('nowrite'):
        return
    file = '_Start.java'
    try:
        startFile = open('{}/{}'.format(dst, file), 'w')
    except:
        death('failure opening {} for writing'.format(file))
    startString = """\
public abstract class _Start {{

    public static _Start parse(Scan scn, Trace trace) {{
        return {start}.parse(scn, trace);
    }}

    public void $run() {{
        System.out.println(this.toString());
    }}

    public void $ok() {{
        System.out.println("OK");
    }}

}}
""".format(start=nt2cls(startSymbol))
    print(startString, file=startFile)
    startFile.close()

def semFinishUp(stubs, destFlag='destdir', ext='.java'):
    if getFlag('nowrite'):
        return
    global STD
    dst = getFlag(destFlag)
    if not dst:
        death('illegal destdir flag value')
    try:
        os.mkdir(str(dst))
        debug('[semFinishUp] ' + dst + ': destination subdirectory created')
    except FileExistsError:
        debug('[semFinishUp] ' + dst + ': destination subdirectory exists')
    except:
        death(dst + ': error creating destination subdirectory')
    print('\n{} source files created:'.format(dst))
    # print *all* of the generated files
    for cls in sorted(stubs):
        if cls in STD:
            death('{}: reserved class name'.format(cls))
        try:
            fname = '{}/{}{}'.format(dst, cls, ext)
            with open(fname, 'w') as f:
                print(stubs[cls], end='', file=f)
        except:
            death('cannot write to file {}'.format(fname))
        print('  {}{}'.format(cls, ext))

def sem(nxt, stubs,
        semFlag,
        lineComment,
        blockCommentStart,
        blockCommentEnd,
        destFlag,
        fileExt,
        **ignored_kwargs):
    global argv
    # print('=== semantic routines')
    if not getFlag(semFlag):
        semFinishUp(stubs, destFlag, fileExt)
        done()
    for line in nxt:
        line = line.strip()
        if line == "%":
            break
        if len(line) == 0 or line[0] == '#':
            # skip just comments or blank lines
            continue
        (cls, _, mod) = line.partition(':')
        # print('>>> cls={} mod={}'.format(cls, mod))
        cls = cls.strip()
        codeString = getCode(nxt) # grab the stuff between %%% ... %%%
        if line[-8:] == ':ignore!':
            continue
        # check to see if line has the form Class:mod
        mod = mod.strip() # mod might be 'import', 'top', etc.
        if cls in stubs:
            if mod and mod != 'ignore' and mod != 'top':
                codeString = '\n'.join(indent(2,codeString))
            else:
                codeString = '\n'.join(indent(1,codeString))
        else:
            codeString = '\n'.join(codeString)
        if mod:
            if cls == '*': # apply the mod substitution to *all* of the stubs
                for cls in stubs:
                    stub = stubs[cls]
                    repl = '{}{}:{}{}'.format(lineComment,cls,mod,lineComment)
                    stub = stub.replace(repl, '{}\n{}'.format(codeString,repl))
                    repl = "{}{}:{}{}".format(blockCommentStart, cls, mod, blockCommentEnd)
                    stub = stub.replace(repl, '{} {}'.format(codeString,repl))
                    debug('class {}:\n{}\n'.format(cls, stub))
                    stubs[cls] = stub
                continue
        if not isClass(cls):
            deathLNO('{}: ill-defined class name'.format(cls))
        if cls in stubs:
            stub = stubs[cls]
            if mod:
                repl = '{}{}:{}{}'.format(lineComment,cls,mod,lineComment)
                stub = stub.replace(repl, '{}\n{}'.format(codeString,repl))
                repl = '{}{}:{}{}'.format(blockCommentStart,cls,mod,blockCommentEnd)
                stub = stub.replace(repl, '{} {}'.format(codeString,repl))
            else: # the default
                repl = '{}{}{}'.format(lineComment,cls,lineComment)
                stub = stub.replace(repl, '{}\n\n{}'.format(codeString,repl))
            debug('class {}:\n{}\n'.format(cls, stub))
            stubs[cls] = stub
        else:
            if mod:
                deathLNO('no stub for class {} -- cannot replace {}{}:{}{}'.format(cls,lineComment,cls,mod,lineComment))
            stubs[cls] = codeString
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


#####################
# utility functions #
#####################

def done():
    exit(0)

def nextLine():
    # create a generator to get the next line in the current input file
    global Lno, Fname, Line
    global stack # used for '%include ...' processing
    global argv  # file arguments
    global nlgen # next line generator for Fname
    maxStack = 4 # maximum %include stacking level
    stack = []
    # debug('...here...')
    while True:
        if len(stack) > 0:
            # pop any %include parent off the stack (stack is initially empty)
            (Fname, Lno, nlgen) = stack.pop()
            debug('back to reading from file ' + Fname)
        elif len(argv) > 0:
            # get the next command line filename
            Fname = argv[0]
            nlgen = nextLineGen(Fname) # resets Lno to zero
            argv = argv[1:] # advance to next filename parameter
        else:
            return None # nothing left!!
        while True:
            try:
                Line = next(nlgen)
                if Line == None:
                    debug('exiting current nextLineGen')
                    break
                Line = Line.rstrip()
                debug('[{}]: {}'.format(Fname, Line))
                # Line is the next line in this file
                # first handle '%include ...' directives
                if lineMode:
                    pass # don't process %include directives  when in line mode
                else:
                    if Line[:8] == '%include':
                        ary = Line.split(None, maxsplit = 1)
                        if len(ary) == 2 and ary[0] == '%include':
                            if len(stack) >= maxStack:
                                death('max %include nesting depth exceeded')
                            debug('include directive: {} {}'
                                  .format(ary[0],ary[1]))
                            # ary[1] must be a filename
                            stack.append((Fname, Lno, nlgen))
                            Fname = ary[1].strip()
                            # print('### now reading from file '+Fname)
                            nlgen = nextLineGen(Fname)
                            continue
                        else:
                            death(line + ': invalid %include directive')
                line = Line.rstrip()
                debug('{:4} [{}] {}'.format(Lno,Fname,Line), level=2)
                yield line
            except:
                break


# next line generator for fname
def nextLineGen(fname):
    global Lno
    debug('creating a nextLineGen generator for file ' + fname)
    if fname == '-':
        fname = 'STDIN'
        f = sys.stdin
    else:
        try:
            f = open(fname, 'r')
        except:
            death(fname + ': error opening file')
    Lno = 0
    debug('now reading from file ' + fname)
    for Line in f:
        Lno += 1
        yield Line
    f.close

def processFlag(flagSpec):
    global flags
    # flagSpec has been stripped
    (key,ee,val) = flagSpec.partition('=')
    key = key.rstrip()
    if re.match(r'[a-zA-Z]\w*$', key) == None:
        raise Exception('malformed flag specification: !' + flagSpec)
    val = val.lstrip()
    # '!key' makes key true, whereas '!key=' makes key false
    if ee == '':     # missing '='
        val = True
    elif val == '':  # empty val
        val = False
    # treat the debug flag specially
    if key == 'debug':
        if val == False:
            val = 0
        elif val == True:
            val = 1
        else:
            try:
                val = int(val)
                if val < 0:
                    val = 0
            except:
                # deathLNO('improper debug flag value')
                raise Exception('improper debug flag value')
    flags[key] = val
    # print(flags)

def getFlag(s):
    global flags
    if s in flags:
        return flags[s]
    else:
        return None

def death(msg):
    print(msg, file=sys.stderr)
    exit(1)

def deathLNO(msg):
    global Lno, Fname, Line
    print('{:4} [{}]: {}'.format(Lno, Fname, msg), file=sys.stderr)
    print('line:', Line, file=sys.stderr)
    exit(1)

def push(struct, item):
    struct.append(item)

def defang(item):
    # item is either <xxx>, <xxx>:?yyy, or neither
    # xxx must be a nonterm or a token name
    global term # all token names
    debug('[defang] item={}'.format(item))
    m = re.match(r'<(\w*#?)>(:?\w*)$', item)
    if m:
        xxx = m.group(1)
        yyy = m.group(2)
        if xxx == '':
            xxx = '$LINE';
        elif isTerm(xxx) or isNonterm(xxx):
            pass
        else:
            deathLNO('malformed "<{}>" in BNF item {}'.format(xxx, item))
        if yyy == '':
            return (xxx, None) # no annotation
        # yyy is nonempty here
        if yyy[0] == ':':
            yyy = yyy[1:] # ditch the ':' part of yyy
        if yyy == '':
            deathLNO('missing annotation in BNF item {}'.format(item))
        if isClass(yyy) or isID(yyy):
            pass
        else:
            deathLNO('malformed annotation "{}" in BNF item {}'.format(yyy, item))
        return (xxx, yyy)
    else: # item must be a bare token
        if not isTerm(item):
            deathLNO('malformed BNF item {}'.format(item))
        if not item in term:
            deathLNO('unknown token name "{}" in BNF rule'.format(item))
        return (None, None)

def defangLHS(lhs):
    # lhs must be either <nt> or <nt>:?cls
    # where nt is a nonterminal and cls is a class name
    nt, cls = defang(lhs)
    if not isNonterm(nt):
        deathLNO('illegal nonterminal "<{}>" in BNF LHS {}'.format(nt, lhs))
    # nt must be a nonterm here
    if cls != None and not isClass(cls):
        deathLNO('illegal class name "{}" in BNF LHS {}'.format(cls, lhs))
    return (nt, cls)

def defangRHS(item):
    # item must be either a token, <tnt>,  or <tnt>:?field
    # where tnt is a token or nonterminal and field is a field name
    # returns (None, None) if item is a token
    # returns (tnt, field) otherwise, where field is derived implicitly from tnt
    #   or field is explicitly given
    tnt, field = defang(item)
    if tnt == None:
        # item is a bare token
        return (None, None)
    if field != None and not isID(field):
        deathLNO('illegal field name "{}" in BNF RHS item {}'.format(field, item))
    # at this point, tnt is either a token or nonterm
    if isTerm(tnt):
        # tnt is a token
        if field == None:
            field = tnt.lower() # derive the field name from the token name
    elif isNonterm(tnt):
        # tnt is a nonterminal
        if field == None:
            field = tnt # set the field name to the nonterminal name
    else:
        deathLNO('"{}" must be a token or nonterm in BNF RHS item {}'.format(tnt,item))
    return (tnt, field)

def isID(item):
    return re.match(r'[a-z]\w*#?$', item)

def isNonterm(nt):
    debug('[isNonterm] nt={}'.format(nt))
    if nt == 'void' or len(nt) == 0:
        return False
    return re.match(r'[a-z]\w*#?$', nt)

def isClass(cls):
    return re.match(r'[A-Z][\$\w]*$', cls) or cls == 'void'

def isTerm(term):
    return re.match(r'[A-Z][A-Z\d_$]*$', term) or term == '$LINE'

def nt2cls(nt):
    # return the class name of the nonterminal nt
    return nt[0].upper() + nt[1:]

def removeOffset(ln, offset):
    check = ln.strip()
    if len(check) == 0:
        return ln
    s = re.sub(offset,"",ln,count=1)
    return s

def getOffset(line):
    check = line.lstrip()
    if len(check) == 0 or check[0] == '#':
        return None
    s = re.search(r"\S", line).start()
    return line[0:s]

if __name__ == '__main__':
    main()
