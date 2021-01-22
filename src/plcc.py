# -*-python-*-


"""
    PLCC: A Programming Languages Compiler-Compiler
    Copyright (C) 2020  Timothy Fossum <plcc@pithon.net>

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
import io
import shutil
import pipes
import tempfile

argv = sys.argv[1:] # skip over the command-line argument

# current file information
Lno = 0             # current line number
Fname = ''          # current file name (STDIN if standard input)
Line = ''           # current line in the file
STD = []            # reserved names from Std library classes
STDT = []           # token-related files in the Std library directory
STDP = []           # parse-related files in the Std library directory

flags = {}          # processing flags (dictionary)

startSymbol = ''    # start symbol (first nonterm in rules)
term = set()        # set of term (token) names
termSpecs = []      # term (token) specifications for generating the Token file

nonterms = set()    # set of all nonterms
fields = {}         # maps a non-abstract class name to its list of fields
rules = []          # list of items  of the form (nt, cls, rhs), one for each grammar rule
extends = {}        # maps a derived class to its abstract base class
derives = {}        # maps an abstract class to a list of its derived classes
cases = {}          # maps a non-abstract class to its set of case terminals for use in a switch
arbno = {}          # maps an arbno class name to its separator string (or None)
stubs = {}          # maps a class name to its parser stub file

def debug(msg, level=1):
    # print(getFlag('debug'))
    if msg and getFlag('debug') >= level:
        print('>>> {}'.format(msg), file=sys.stderr)
        return True
    return False

def debug2(msg):
    debug(msg, level=2)

def LIBPLCC():
    try:
        return os.environ['LIBPLCC']
    except KeyError:
        return '/usr/local/pub/plcc/PLCC' ######## System specific! ########

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
        from pathlib import Path
        version_file = Path(__file__).resolve().parent / 'VERSION'
        with open(version_file, 'r') as f:
            contents = f.read()
            print("PLCC " + contents.strip())
        sys.exit(0)

    nxt = nextLine()     # nxt is the next line generator
    lex(nxt)    # lexical analyzer generation
    par(nxt)    # LL(1) check and parser generation
    sem(nxt)    # semantic actions

def plccInit():
    global flags, STD, STDT, STDP
    STDT = ['ILazy','IMatch','ITrace','IScan','Trace','Scan']
    STDP = ['Parser','Rep']
    STD = STDT + STDP
    STD.append('Token')
    # file-related flags -- can be overwritten
    # by a grammar file '!flag=...' spec
    # or by a '--flag=...' command line argument
    for fname in STD:
        flags[fname] = fname
    flags['libplcc'] = LIBPLCC()
    flags['Token'] = True
    # behavior-related flags
    flags['PP'] = ''              # preprocessor cmd (e.g., 'cpp -P')
    flags['debug'] = 0            # default debug value
    flags['destdir'] = 'Java'     # the default destination directory
    flags['pattern'] = True       # create a scanner that uses re. patterns
    flags['LL1'] = True           # check for LL(1)
    flags['parser'] = True        # create a parser
    flags['semantics'] = True     # create semantics routines
    flags['nowrite'] = False      # when True, produce *no* file output

def lex(nxt):
    # print('=== lexical specification')
    for line in nxt:
        if line == '%':
            break
        line = line.lstrip()
        if len(line) == 0 or line[0] == '#': # skip empty lines and comments
            continue
        line = re.sub('\s+#.*$', '', line)   # remove trailing comments ...
        line = line.rstrip()                 # ... and any remaining whitespace
        # print ('>>> {}'.format(line))
        jpat = '' # the Java regular expression pattern for this skip/term
        pFlag = getFlag('pattern')
        if pFlag:
            # handle capturing the match part and replacing with empty string
            def qsub(match):
                nonlocal jpat
                if match:
                    jpat = match.group(1)
                    # print('>>> match found: jpat={}'.format(jpat))
                return ''
            pat = "\s'(.*)'$"
            # print('>>> q1 pat={}'.format(pat))
            line = re.sub(pat, qsub, line)
            if jpat:
                # add escapes to make jpat into a Java string
                jpat = re.sub(r'\\', r'\\\\', jpat)
                jpat = re.sub('"', r'\\"', jpat)
                # print('>>> q1 match found: line={} jpat={}'.format(line,jpat))
                pass
            else:
                pat = '\s"(.*)"$'
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
        line = line.strip()
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
            skip = ', true'   # Java boolean constant
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
        os.mkdir(dst)
        debug('[lexFinishUp] ' + dst + ': destination subdirectory created')
    except FileExistsError:
        debug('[lexFinishUp] ' + dst + ': destination subdirectory exists')
    except:
        death(dst + ': error creating destination subdirectory')
    if not getFlag('Token'):
        return # do not create any automatically generated scanner-related files
    libplcc = getFlag('libplcc')
    if not libplcc:
        death('illegal libplcc flag value')
    std = libplcc + '/Std'
    try:
        os.mkdir(std)
    except FileExistsError:
        pass
    except:
        death(std + ': cannot access directory')
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
            if re.match('^\s*%%Vals%%', line):
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
            if re.match('^\s*%%Vals%%', line):
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
        if line == '%':
            break
        line = line.lstrip() # clobber leading whitespace
        line = re.sub('#.*$', '', line) # remove comments
        line = line.rstrip()            # clobber any trailing whitespace
        if line == '':
            continue                    # skip entirely blank lines
        # if re.search('_', line):
        #     deathLNO('underscore "_" not permitted in grammar rule line')
        rno += 1
        processRule(line, rno)
    parFinishUp()

def parFinishUp():
    global STDP, startSymbol, nonterms, extends, derives, rules
    if not rules:
        print('No grammar rules', file=sys.stderr)
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
            continue           # ignore automatically generated arbno names
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
    std = libplcc + '/Std'
    for fname in STDP:
        if getFlag(fname):
            debug('[parFinishUp] copying {} from {} to {} ...'.format(fname, std, dst))
            try:
                shutil.copy('{}/{}.java'.format(std, fname), '{}/{}.java'.format(dst, fname))
            except:
                death('Failure copying {} from {} to {}'.format(fname, std, dst))

    # build parser stub classes
    buildStubs()
    # build the PLCC$Start.java file from the start symbol
    buildStart()

def processRule(line, rno):
    global STD, startSymbol, fields, rules, arbno, nonterm, extends, derives
    if rno:
        debug('[processRule] rule {:3}: {}'.format(rno, line))
    tnt = line.split()     # LHS ruleType RHS
    if len(tnt) < 2:
        deathLNO('illegal grammar rule') # no ruleType
    lhs = tnt.pop(0)       # the LHS of this rule
    nt, cls = partitionLHS(lhs)
    base = nt2cls(nt)      # the base (class) name of this nonterminal
    if base in STD:
        deathLNO('{}: reserved class name'.format(base))
    if cls in STD:
        deathLNO('{}: reserved class name'.format(cls))
    if base == cls:
        deathLNO('base class and derived class names cannot be the same!')
    ruleType = tnt.pop(0)  # either '**=' or '::='
    rhs = tnt              # a list of all the items to the right
                           # of the ::= or **= on the line
    if ruleType == '**=':  # this is an arbno rule
        if cls:
            deathLNO('arbno rule cannot specify a non base class name')
        if startSymbol == '':
            deathLNO('arbno rule cannot be the first grammar rule')
        if len(rhs) == 0:
            deathLNO('arbno rules cannot be empty')
        debug('[processRule] arbno: ' + line)
        sep = rhs[-1] # get the last entry in the line
        if sep[0] == '+':
            # must be a separated list
            sep = sep[1:] # remove the leading '+' from the separator
            if not isTerm(sep):
                deathLNO('final separator in an arbno rule must be a Terminal')
            rhs.pop()       # remove separator from the rhs list
        else:
            sep = None
        # arbno rule has no derived classes, so it's just a base class
        # saveFields(base, lhs, rhs) # check for duplicate classes,
        # then map the base to its (lhs, rhs) pair
        arbno[base] = sep   # mark base as an arbno class with separator sep
                            # (possibly None)
        # next add non-arbno rules to the rule set to simulate arbno rules
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
    # at this point, we may have a legal non-arbno rule
    debug('[processRule] so far: {} ::= {}'.format(lhs, rhs))
    nonterms.update({nt}) # add nt to the set of LHS nonterms
    if cls == 'void':
        # this rule is *generated* by an arbno rule,
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

# def saveFields(cls, lhs, rhs):
#     global fields
#     if cls in fields:
#         deathLNO('class {} is already defined'.format(cls))
#    fields[cls] = (lhs, rhs)

def saveRule(nt, lhs, cls, rhs):
    """ construct a tuple of the form (nt, tnts) where nt is the LHS nonterm (minus the <>)
        and tnts is a list of the terminal/nonterm items extracted from the rhs
        (and excluding their field names).  Then add this to the rules list for determining LL1.
        Also, map fields[cls] to the (lhs, rhs) pair
    """
    global rules, fields
    if cls != None:
        if cls in fields:
            deathLNO('class {} is already defined'.format(cls))
        if cls in arbno:
            fields[cls] = (lhs, rhs[:-1]) # remove the item with the underscore
        else:
            fields[cls] = (lhs, rhs)
    tnts = []
    for item in rhs:
        tnts.append(defangg(item)[0])
    rules.append((nt, cls, tnts)) # add the rule tuple to the rules list

def partitionLHS(lhs):
    # split the lhs string <xxx>[:yyy] and return xxx, yyy
    # if :yyy is missing, return xxx, None
    # xxx must be a legal nonterm name,
    # and yyy (if present) must be either 'void' or a legal class name
    nt, c, cls = lhs.partition(':')
    if c == '':
        cls = None   # :yyy part is not present
    elif cls == '':  # :yyy is present, but yyy is empty
        deathLNO('illegal LHS: ' + lhs)
    ntt = defang(nt) # extract xxx (remove '<' and '>')
    if ntt == '':
        deathLNO('missing nonterminal')
    if ntt == 'void':
        deathLNO('cannot use "void" as a nonterminal in LHS {}'.format(lhs))
    if '<{}>'.format(ntt) == nt and isNonterm(ntt):
        pass         # OK format
    else:
        deathLNO('illegal nonterminal format {} in LHS {}'.format(nt, lhs))
    if cls == None or cls == 'void' or isClass(cls):
        pass         # OK cls
    else:
        deathLNO('illegal class name {} in LHS {}'.format(cls, lhs))
    return ntt, cls

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

def buildStubs():
    global fields, derives, stubs
    for cls in derives:
        # make parser stubs for all abstract classes
        if cls in stubs:
            death('duplicate stub for abstract class {}'.format(cls))
        debug('[buildStubs] making stub for abstract class {}'.format(cls))
        stubs[cls] = makeAbstractStub(cls)
    for cls in fields:
        # make parser stubs for all non-abstract classes
        if cls in stubs:
            death('duplicate stub for class {}'.format(cls))
        debug('[buildStubs] making stub for non-abstract class {}'.format(cls))
        stubs[cls] = makeStub(cls)

def makeAbstractStub(base):
    global cases
    caseList = []    # a list of strings, either 'case XXX:' or '    return Cls.parse(...);'
    for cls in derives[base]:
        if len(cases[cls]) == 0:
            death('class {} is unreachable'.format(cls))
        for tok in cases[cls]:
            caseList.append('case {}:'.format(tok))
        caseList.append('    return {}.parse(scn$,trace$);'.format(cls))
    if base == nt2cls(startSymbol):
        dummy = '\n    public {}() {{ }} // dummy constructor\n'.format(base)
    else:
        dummy = ''
    stubString = """\
//{base}:top//
//{base}:import//
import java.util.*;

public abstract class {base} {{
{dummy}
    public static {base} parse(Scan scn$, Trace trace$) {{
        Token t$ = scn$.cur();
        Token.Val v$ = t$.val;
        switch(v$) {{
{cases}
        default:
            throw new RuntimeException("{base} cannot begin with " + v$);
        }}
    }}

//{base}//

}}
""".format(cls=cls, base=base, dummy=dummy, cases='\n'.join(indent(2, caseList)))
    return stubString

def makeStub(cls):
    global fields, extends, arbno
    # make a stub for the given non-abstract class
    debug('[makeStub] making stub for non-abstract class {}'.format(cls))
    sep = False
    (lhs, rhs) = fields[cls]
    ext = '' # assume not an extended class
    # two cases: either cls is an arbno rule, or it isn't
    if cls in arbno:
        ruleType = '**='
        sep = arbno[cls]
        (fieldVars, parseString) = makeArbnoParse(cls, rhs, sep)
        if sep != None:
            rhs = rhs + ['+{}'.format(sep)]
    else:
        ruleType = '::='
        (fieldVars, parseString) = makeParse(cls, rhs)
        # two sub-cases: either cls is an extended class (with abstract base class) or it's a base class
        if cls in extends:
            ext = ' extends ' + extends[cls]
        else:
            pass
    ruleString = '{} {} {}'.format(lhs, ruleType, ' '.join(rhs))
    # fieldVars = makeVars(cls, rhs)
    decls = []
    inits = []
    params = []
    for (field, fieldType) in fieldVars:
        decls.append('public {} {};'.format(fieldType, field))
        inits.append('this.{} = {};'.format(field, field))
        params.append('{} {}'.format(fieldType, field))
    debug('[makeStub] cls={} decls={} params={} inits={}'.format(cls, decls, params, inits))
    debug('[makeStub] rule: {}'.format(ruleString))
    if cls == nt2cls(startSymbol) and params:
        dummy = '\n    public {}() {{ }} // dummy constructor\n'.format(cls)
    else:
        dummy = ''
    stubString = """\
import java.util.*;
//{cls}:import//

// {ruleString}
public class {cls}{ext} {{

{decls}
{dummy}
    public {cls}({params}) {{
{inits}
    }}

    public static {cls} parse(Scan scn$, Trace trace$) {{
        if (trace$ != null)
            trace$ = trace$.nonterm("{lhs}", scn$.lno);
{parse}
    }}

//{cls}//

}}
""".format(cls=cls,
           lhs=lhs,
           ext=ext,
           ruleString=ruleString,
           decls='\n'.join(indent(1, decls)),
           dummy=dummy,
           params=', '.join(params),
           inits='\n'.join(indent(2, inits)),
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
    for item in rhs:
        (tnt, field) = defangg(item)
        if field == None:
            parseList.append('scn$.match(Token.Val.{}, trace$);'.format(tnt))
            continue
        if field in fieldSet:
            death('duplicate field name {} in rule RHS {}'.format(field, ' '.join(rhs)))
        fieldSet.update({field})
        args.append(field)
        if isTerm(tnt):
            fieldType = 'Token'
            parseList.append('Token {} = scn$.match(Token.Val.{}, trace$);'.format(field, tnt))
        else:
            fieldType = nt2cls(tnt)
            parseList.append('{} {} = {}.parse(scn$, trace$);'.format(fieldType, field, fieldType))
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
    fieldSet = set() # the set of field variable names
    # rhs = rhs[:-1]   # remove the last item from the grammar rule (which has an underscore item)
    # create the parse statements to be included in the loop
    switchCases = [] # the token cases in the switch statement
    for item in rhs:
        (tnt, field) = defangg(item)
        if field == None:
            # a bare token -- match it
            loopList.append('scn$.match(Token.Val.{}, trace$);'.format(tnt))
            continue
        if field in fieldSet:
            death('duplicate field name {} in rule RHS {}'.format(field, ' '.join(rhs)))
        fieldSet.update({field})
        field += 'List'
        args.append(field)
        if isTerm(tnt):
            # a term (token)
            baseType = 'Token'
            loopList.append('{}.add(scn$.match(Token.Val.{}, trace$));'.format(field, tnt))
        else:
            # a nonterm
            baseType = nt2cls(tnt)
            loopList.append('{}.add({}.parse(scn$, trace$));'.format(field, baseType))
        fieldType = 'List<{}>'.format(baseType)
        fieldVars.append((field, fieldType))
        inits.append('{} {} = new ArrayList<{}>();'.format(fieldType, field, baseType))
    switchCases = []
    if len(cases[cls]) == 0:
        death('class {} is unreachable'.format(cls))
    for item in cases[cls]:
        switchCases.append('case {}:'.format(item))
    returnItem = 'return new {}({});'.format(cls, ', '.join(args))
    if sep == None:
        # no separator
        parseString = """\
{inits}
        while (true) {{
            Token t$ = scn$.cur();
            Token.Val v$ = t$.val;
            switch(v$) {{
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
        Token.Val v$ = t$.val;
        switch(v$) {{
{switchCases}
            while(true) {{
{loopList}
                t$ = scn$.cur();
                v$ = t$.val;
                if (v$ != Token.Val.{sep})
                    break; // not a separator, so we're done
                scn$.match(v$, trace$);
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
    # build the PLCC$Start.java file
    if startSymbol == '':
        death('no start symbol!')
    dst = getFlag('destdir')
    if dst == None or getFlag('nowrite'):
        return
    file = 'PLCC$Start.java'
    try:
        startFile = open('{}/{}'.format(dst, file), 'w')
    except:
        death('failure opening {} for writing'.format(file))
    startString = """\
public abstract class PLCC$Start extends {start} {{ }}
""".format(start=nt2cls(startSymbol))
    print(startString, file=startFile)
    startFile.close()

def sem(nxt):
    global stubs, argv
    # print('=== semantic routines')
    if not getFlag('semantics'):
        semFinishUp()
        done()
    for line in nxt:
        line = line.strip()
        if line[:7] == 'include':
            # add file names to be processed
            fn = line[7:].split()
            argv.extend(fn)
            # print('== extend argv by {}'.format(fn))
            continue
        if len(line) == 0 or line[0] == '#':
            # skip just comments or blank lines
            continue
        (cls, _, mod) = line.partition(':')
        # print('>>> cls={} mod={}'.format(cls, mod))
        cls = cls.strip()
        codeString = getCode(nxt) # grab the stuff between %%% ... %%%
        if mod:
            mod = mod.strip() # mod is either 'import' or 'top'
            if cls == '*': # apply the mod substitution to *all* of the stubs
                for cls in stubs:
                    stub = stubs[cls]
                    repl = '//{}:{}//'.format(cls, mod)
                    stub = stub.replace(repl, '{}\n{}'.format(codeString,repl))
                    debug('class {}:\n{}\n'.format(cls, stub))
                    stubs[cls] = stub
                continue
        if not isClass(cls):
            deathLNO('{}: ill-defined class name'.format(cls))
        if mod == 'ignore!':
            continue
        if cls in stubs:
            stub = stubs[cls]
            if mod:
                repl = '//{}:{}//'.format(cls, mod)
            else:
                repl = '//{}//'.format(cls)
            stub = stub.replace(repl, '{}\n{}'.format(codeString,repl))
            debug('class {}:\n{}\n'.format(cls, stub))
            stubs[cls] = stub
        else:
            if mod:
                deathLNO('no stub for class {} -- cannot replace //{}:{}//'.format(cls, cls, mod))
            stubs[cls] = codeString
    semFinishUp()
    done()

def getCode(nxt):
    code = []
    for line in nxt:
        line = line.rstrip()
        if re.match(r'\s*#', line) or re.match(r'\s*$', line):
            # skip comments or blank lines
            continue
        if re.match(r'\s*%%{', line): # legacy plcc
            stopMatch = r'\s*%%}'
            break
        if re.match(r'\s*%%%', line):
            stopMatch = r'\s*%%%'
            break
        else:
            deathLNO('expecting a code segment')
    for line in nxt:
        if re.match(stopMatch, line):
            break
        code.append(line)
    else:
        deathLNO('premature end of file')
    str = '\n'.join(code)
    return str

def semFinishUp():
    if getFlag('nowrite'):
        return
    global stubs, STD
    dst = flags['destdir']
    print('\nJava source files created:')
    cmd = getFlag('PP') # run a preprocessor, if specified
    for cls in sorted(stubs):
        if cls in STD:
            death('{}: reserved class name'.format(cls))
        try:
            fname = '{}/{}.java'.format(dst, cls)
            if len(cmd) > 0:
                t = pipes.Template()
                # print('>>> adding {} preprocessor to the pipe'.format(cmd))
                t.append(cmd, '--')
                # print('>>> writing to file {}'.format(fname))
                with t.open(fname, 'w') as f:
                    print(stubs[cls], end='', file=f)
            else:
                with open(fname, 'w') as f:
                    print(stubs[cls], end='', file=f)
        except:
            death('cannot write to file {}'.format(fname))
        print('  {}.java'.format(cls))

#####################
# utility functions #
#####################

def done(msg=''):
    if msg:
        print(msg, file=sys.stderr)
    exit(0)

def nextLine():
    # create a generator to get the next line in the current input file
    global Lno, Fname, Line
    for Fname in argv:
        # open the next input file
        f = None # the current open file
        if Fname == '-':
            f = sys.stdin
            Fname = 'STDIN'
        else:
            try:
                f = open(Fname, 'r')
            except:
                death(Fname + ': error opening file')
        Lno = 0
        # f is the current open file
        for Line in f:
            # get the next line in this file
            Lno += 1
            line = Line.rstrip()
            if len(line) > 0 and line[0] == '!':
                line = line[1:]
                # print ('>>> flag line: {}'.format(line))
                try:
                    processFlag(line)
                except Exception as msg:
                    deathLNO(msg)
                continue
            debug('{:4} [{}] {}'.format(Lno,Fname,Line), level=2)
            yield line
        f.close()

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

def defang(exp):
    # if exp is of the form '<xxx>', return xxx
    # otherwise leave alone
    match = re.match('<(.+)>$', exp)
    if match:
        return match.group(1)
    return exp

def defangg(item):
    """
    item format      returns
    -----------      -------
    PQR              (PQR, None)
    <pqr>            (pqr, pqr)
    <PQR>            (PQR, pqr)  # pqr is PQR in lowercase
    <pqr>stu         (pqr, stu)
    <PQR>stu         (PQR, stu)
                     death in any other cases
    pqr is a nonterm (possibly ending with '#') and PQR is a term (token).
    The first item in the returned tuple is either a Nonterm or a Term
    The second item in the tuple is either None or an identifier
    starting in lowercase
    """
    tnt = None
    field = None
    debug('[defangg] item={}'.format(item))
    m = re.match(r'<([^>]*)>(.*)$', item)
    if m:
        tnt = m.group(1)
        field = m.group(2)
        if field == '':
            if isTerm(tnt):
                field = tnt.lower()
            else:
                field = tnt
    else:
        m = re.match('\w+#?$', item)
        if m:
            tnt = item
            field = None
    # just check for legal values (done once)
    if tnt == None or tnt == '':
        deathLNO('malformed RHS grammar item {}'.format(item))
    if not isTerm(tnt) and not isNonterm(tnt):
        deathLNO('malformed RHS grammar item {}'.format(item))
    if isTerm(tnt) and not tnt in term:
        deathLNO('unknown token name in RHS grammar item {}'.format(item))
    if field == None:
        if not isTerm(tnt):
            deathLNO('cannot have a bare nonterm in RHS grammar item {}'.format(item))
    elif not isID(field):
        deathLNO('field {} is an invalid identifier in RHS grammar item {}'.format(field, item))
    return (tnt, field)

def isID(item):
    return re.match('[a-z]\w*#?$', item)

def isNonterm(nt):
    debug('[isNonterm] nt={}'.format(nt))
    if nt == 'void' or len(nt) == 0:
        return False
    return re.match('[a-z]\w*#?$', nt)

def isClass(cls):
    return cls == 'void' or re.match('[A-Z][\$\w]*$', cls)

def isTerm(term):
    return re.match('[A-Z][A-Z\d_]*$', term)

def nt2cls(nt):
    # return the class name of the nonterminal nt
    return nt[0].upper() + nt[1:]

if __name__ == '__main__':
    main()
