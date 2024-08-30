from .error import ParseError
from ..spec.syntactic import SyntacticSpec


def parseSyntacticSpec(sectionLines, lexicalSpec):
    p = SyntacticParser(lexicalSpec)
    p.parse(sectionLines)
    spec = p.getSyntacticSpec()
    spec.validate()
    return spec


class SyntacticParser():
    def __init__(self, lexicalSpec):
        self._lexicalSpec = lexicalSpec

        self._reservedNames = [
            'ILazy',
            'IMatch',
            'IScan',
            'ITrace',
            'Trace',
            'PLCCException',
            'Scan',
            'ProcessFiles',
            'Parse',
            'Rep',
            'ParseJsonAst',
            'Token'
        ]

        self._startSymbol = ''
        self._fields = {}   # maps a non-abstract class name to its list of fields
        self._rrule = {}    # maps a repeating rule class name to its separator string
                            # (or None)
        self._extends = {}  # maps a derived class to its abstract base class
        self._derives = {}  # maps an abstract class to a list of its derived classes
        self._rules = []    # list of items  of the form (nt, cls, rhs),
                            # one for each grammar rule
        self._terminalSet = set()
        self._nonterminalSet = set()


    def parse(self, sectionLines):
        for line_obj in sectionLines:
            try:
                line = line_obj.text
                line = re.sub('#.*$', '', line) # remove comments
                line = line.strip()
                if len(line) == 0:
                    continue                    # skip entirely blank lines
                if line == '%':
                    break
                self._processRule(line)
            except Exception as e:
                raise ParseError(line_obj, str(e))

    def _processRule(self, line):
        tnt = line.split()     # LHS ruleType RHS
        if len(tnt) < 2:
            raise Exception('illegal grammar rule')
        lhs = tnt.pop(0)       # the LHS of this rule
        nt, cls = self._defangLHS(lhs)
        base = self._nt2cls(nt)      # the base (class) name of this nonterminal
        if base == cls:
            raise Exception('base class and derived class names cannot be the same!')
        if self._isReserved(base):
            raise Exception(f'{base}: reserved class name')
        if cls != None and self._isReserved(cls):
            raise Exception(f'{cls}: reserved class name')
        ruleType = tnt.pop(0)  # either '**=' or '::='
        rhs = tnt              # a list of all the items to the right
                            # of the ::= or **= on the line
        if ruleType == '**=':  # this is a repeating rule
            if cls != None:
                raise Exception('repeating rule cannot specify a non base class name')
            if self._startSymbol == '':
                raise Exception('repeating rule cannot be the first grammar rule')
            if len(rhs) == 0:
                raise Exception('repeating rules cannot be empty')
            sep = rhs[-1] # get the last entry in the line
            if sep[0] == '+':
                # must be a separated list
                sep = sep[1:]   # remove the leading '+' from the separator
                if not self._isValidTerm(sep):
                    raise Exception(f'separator {sep} in repeating rule must be a bare Token')
                rhs.pop()       # remove separator from the rhs list
            else:
                sep = None
            # a repeating rule has no derived classes, so it's just a base class
            # saveFields(base, lhs, rhs) ?? check for duplicate classes,
            # then map the base to its (lhs, rhs) pair
            self._rrule[base] = sep   # mark base as a repeating rule class with separator sep
                                # (possibly None)
            # next add right-recursive rules to the rule set to simulate repeating rules
            rhsString = ' '.join(rhs)
            if sep:
                ntsep = nt+'#'  # 'normal' nonterms cannot have '#' symbols
                self._processRule('<{}>      ::= {} <{}>'.format(nt, rhsString, ntsep), None)
                self._processRule('<{}>:void ::='.format(nt), None)
                self._processRule('<{}>:void ::= {} {} <{}>'.format(ntsep, sep, rhsString, ntsep), None)
                self._processRule('<{}>:void ::='.format(ntsep), None)
            else:
                self._processRule('<{}>      ::= {} <{}>'.format(nt, rhsString, nt), None)
                self._processRule('<{}>:void ::='.format(nt), None)
            return
        elif not ruleType == '::=':
            raise Exception('illegal grammar rule syntax')
        # at this point, we may have a legal non-repeating rule
        self._nonterminalSet.update({nt}) # add nt to the set of LHS nonterms
        if cls == 'void':
            # this rule is *generated* by a repeating rule,
            # so there are no further class-related actions to do
            self._saveRule(nt, lhs, None, rhs)
            return
        if self._startSymbol == '':
            self._startSymbol = nt   # the first lhs nonterm is the start symbol
        if cls == None:
            # a simple base class -- no derived classes involved
            self._saveRule(nt, lhs, base, rhs)
            return
        # if we get here, cls (non-abstract) is a new class derived from base (abstract)
        if cls in self._derives:
            raise Exception(f'non-abstract class {cls} is already defined as an abstract class')
        if base in self._fields:
            raise Exception(f'abstract base class {base} already exists as a non-abstract class')
        self._saveRule(nt, lhs, cls, rhs)
        self._extends[cls] = base
        if base in self._derives:
            self._derives[base].update({cls})
        else:
            self._derives[base] = {cls}

    def _isReserved(self, name):
        return name in self._reservedNames

    def _saveRule(self, nt, lhs, cls, rhs):
        """ construct a tuple of the form (nt, tnts) where nt is the LHS nonterm
            (minus the <>) and tnts is a list of the terminal/nonterm items
            extracted from the rhs (and excluding their field names).
            Then add this to the rules list for determining LL1.
            Also, map fields[cls] to the (lhs, rhs) pair
        """
        if cls != None:
            if cls in self._fields:
                raise Exception(f'class {cls} is already defined')
            if cls in self._rrule:
                self._fields[cls] = (lhs, rhs[:-1]) # remove the separator token
            else:
                self._fields[cls] = (lhs, rhs)
        tnts = []
        for item in rhs:
            tnt, field = self._defangRHS(item)
            if tnt == None: # item is a bare token
                tnt = item;
            tnts.append(tnt) # tnt may be a nonterm or a token name
        self._rules.append((nt, cls, tnts)) # add the rule tuple to the rules list

    def _defangLHS(self, lhs):
        # lhs must be either <nt> or <nt>:?cls
        # where nt is a nonterminal and cls is a class name
        nt, cls = self._defang(lhs)
        if not self._isValidNonterminal(nt):
            raise Exception(f'illegal nonterminal "<{nt}>" in BNF LHS {lhs}')
        # nt must be a nonterm here
        if cls != None and not self._isValidClass(cls):
            raise Exception(f'illegal class name "{cls}" in BNF LHS {lhs}')
        return (nt, cls)

    def _defangRHS(self, item):
        # item must be either a token, <tnt>,  or <tnt>:?field
        # where tnt is a token or nonterminal and field is a field name
        # returns (None, None) if item is a token
        # returns (tnt, field) otherwise, where field is derived implicitly from tnt
        #   or field is explicitly given
        tnt, field = self._defang(item)
        if tnt == None:
            # item is a bare token
            return (None, None)
        if field != None and not self._isValidID(field):
            raise Exception(f'illegal field name "{field}" in BNF RHS item {item}')
        # at this point, tnt is either a token or nonterm
        if self._isValidTerm(tnt):
            # tnt is a token
            if field == None:
                field = tnt.lower() # derive the field name from the token name
        elif self._isValidNonterminal(tnt):
            # tnt is a nonterminal
            if field == None:
                field = tnt # set the field name to the nonterminal name
        else:
            raise Exception(f'"{tnt}" must be a token or nonterm in BNF RHS item {item}')
        return (tnt, field)

    def _defang(self, item):
        # item is either <xxx>, <xxx>:?yyy, or neither
        # xxx must be a nonterm or a token name
        m = re.match(r'<(\w*#?)>(:?\w*)$', item)
        if m:
            xxx = m.group(1)
            yyy = m.group(2)
            if xxx == '':
                xxx = '$LINE';
            elif self._isValidTerm(xxx) or self._isValidNonterminal(xxx):
                pass
            else:
                raise Exception(f'malformed "<{xxx}>" in BNF item {item}')
            if yyy == '':
                return (xxx, None) # no annotation
            # yyy is nonempty here
            if yyy[0] == ':':
                yyy = yyy[1:] # ditch the ':' part of yyy
            if yyy == '':
                raise Exception(f'missing annotation in BNF item {item}')
            if self._isValidClass(yyy) or self._isValidID(yyy):
                pass
            else:
                raise Exception(f'malformed annotation "{yyy}" in BNF item {item}')
            return (xxx, yyy)
        else: # item must be a bare token
            if not self._isValidTerm(item):
                raise Exception(f'malformed BNF item {item}')
            if not self._lexicalSpec.isTerminal(item):
                raise Exception(f'unknown token name "{item}" in BNF rule')
            return (None, None)

    def _isValidTerm(self, term):
        return re.match(r'[A-Z][A-Z\d_$]*$', term) or term == '$LINE'

    def _isValidClass(self, cls):
        return re.match(r'[A-Z][\$\w]*$', cls) or cls == 'void'

    def _isValidID(self, item):
        return re.match(r'[a-z]\w*#?$', item)

    def _isValidNonterminal(self, nt):
        if nt == 'void' or len(nt) == 0:
            return False
        return re.match(r'[a-z]\w*#?$', nt)

    def _nt2cls(self, nt):
        # return the class name of the nonterminal nt
        return nt[0].upper() + nt[1:]

    def getSyntacticSpec(self):
        spec = SyntacticSpec()
        spec.initDerives(self._derives)
        spec.initExtends(self._extends)
        spec.initNonterminals(self._nonterminalSet)
        spec.initRules(self._rules)
        spec.initStartSymbol(self._startSymbol)
        return spec




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
    # parsed_fields[cls]

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


@dataclass
class TNT:
    original: str
    tnt: str
    field: str


@dataclass
class Rule:
    lhs_tnt: TNT
    type: str
    rhs_tnts: [TNT]
    sep: str
