def _orphans_from_old_parFinishUp():

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

    buildStubsAndStart(java, python, fields, derives, cases, startSymbol)


def buildStubsAndStart(java, python, fields, derives, cases, startSymbol):
    buildStubs(java, fields, derives, cases, startSymbol)
    buildStubs(python, fields, derives, cases, startSymbol)
    buildStart()





class DuplicateAbstractStubException(Exception):
    pass

class UnreachableClassException(Exception):
    pass

class DuplicateStubException(Exception):
    pass

def buildStubs(stubs, fields, derives, cases, startSymbol):
    for cls in derives:
        # make parser stubs for all abstract classes
        if cls in stubs.getStubs():
            raise DuplicateAbstractStubException(f'{cls}')
        for c in derives[cls]:
            if len(cases[c]) == 0:
                raise UnreachableClassException(f'{c}')
        stubs.addAbstractStub(cls, derives, cases, startSymbol, caseIndentLevel=2, ext=' extends _Start')

    for cls in fields:
        # make parser stubs for all non-abstract classes
        if cls in stubs.getStubs():
            raise DuplicateStubException(f'{cls}')
        makeStub(stubs, cls)


def makeStub(stubs, cls):
    global fields, extends, rrule
    # make a stub for the given non-abstract class
    debug('[makeStub] making stub for non-abstract class {}'.format(cls))
    sep = False
    (lhs, rhs) = fields[cls]
    extClass = '' # assume not an extended class
    # two cases: either cls is a repeating rule, or it isn't
    if cls in rrule:
        ruleType = '**='
        sep = rrule[cls]
        arbno = parseArbno(cls, rhs, cases)
        (fieldVars, parseString) = makeArbnoParse(cls, arbno, sep)
        if sep != None:
            rhs = rhs + ['+{}'.format(sep)]
    else:
        ruleType = '::='
        (fieldVars, parseString) = makeParse(cls, rhs)
        # two sub-cases: either cls is an extended class (with abstract base class) or it's a base class
        if cls in extends:
            extClass = extends[cls]
    ruleString = '{} {} {}'.format(lhs, ruleType, ' '.join(rhs))
    stubs.addStub(cls, fieldVars, startSymbol, lhs, extClass, ruleString, parseString)

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


def parseArbno(cls, rhs, cases):
    rhsString = ' '.join(rhs)
    fieldSet = set() # the set of field variable names for this RHS
    itemTntFields = []
    for item in rhs:
        (tnt, field) = defangRHS(item)
        if tnt is not None:
            field += 'List'
            if field in fieldSet:
                deathLNO(
                    'duplicate field name {} in RHS rule {}'.format(field, rhsString))
            fieldSet.update({field})
        itemTntFields.append( (item, tnt, field) )
    if len(cases[cls]) == 0:
        deathLNO('class {} is unreachable'.format(cls))
    return itemTntFields


def makeArbnoParse(cls, arbno, sep):
    # print('%%%%%% cls={} rhs="{}" sep={}'.format(cls, ' '.join(rhs), sep))
    global cases
    inits = []       # initializes the List fields
    args = []        # the arguments to pass to the constructor
    loopList = []    # the match/parse code in the Arbno loop
    fieldVars = []   # the field variable names (all Lists), to be returned
    # rhs = rhs[:-1]   # remove the last item from the grammar rule (which has an underscore item)
    # create the parse statements to be included in the loop
    switchCases = [] # the token cases in the switch statement

    for item, tnt, field in arbno:
        if tnt == None:
            loopList.append('scn$.match(Token.Match.{}, trace$);'.format(item))
            continue
        # field is either derived from tnt or is an annotated field name
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
        fieldType = 'List<{}>'.format(baseType)
        fieldVars.append((field, fieldType))
        inits.append('{} {} = new ArrayList<{}>();'.format(fieldType, field, baseType))
    switchCases = []
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
