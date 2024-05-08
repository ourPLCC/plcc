from .error import ParseError


def parseSyntacticSpec(sectionLines, lexicalSpec):
    p = SyntacticParser(lexicalSpec)
    p.parse(sectionLines)
    return p.getSyntacticSpec()


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
                if not self._isTerm(sep):
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
            saveRule(nt, lhs, None, rhs)
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
        if not self._isNonterm(nt):
            raise Exception(f'illegal nonterminal "<{nt}>" in BNF LHS {lhs}')
        # nt must be a nonterm here
        if cls != None and not self._isClass(cls):
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
        if field != None and not self._isID(field):
            raise Exception(f'illegal field name "{field}" in BNF RHS item {item}')
        # at this point, tnt is either a token or nonterm
        if self._isTerm(tnt):
            # tnt is a token
            if field == None:
                field = tnt.lower() # derive the field name from the token name
        elif self._isNonterm(tnt):
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
            elif self._isTerm(xxx) or self._isNonterm(xxx):
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
            if self._isClass(yyy) or self._isID(yyy):
                pass
            else:
                raise Exception(f'malformed annotation "{yyy}" in BNF item {item}')
            return (xxx, yyy)
        else: # item must be a bare token
            if not self._isTerm(item):
                raise Exception(f'malformed BNF item {item}')
            if not self._lexicalSpec.isTerminal(item):
                raise Exception(f'unknown token name "{item}" in BNF rule')
            return (None, None)

    def _isTerm(self, term):
        return re.match(r'[A-Z][A-Z\d_$]*$', term) or term == '$LINE'

    def _isClass(self, cls):
        return re.match(r'[A-Z][\$\w]*$', cls) or cls == 'void'

    def _isID(self, item):
        return re.match(r'[a-z]\w*#?$', item)

    def _nt2cls(self, nt):
        # return the class name of the nonterminal nt
        return nt[0].upper() + nt[1:]


    def getSyntacticSpec(self):
        return SyntacticSpec()


class SyntacticSpec:
    ...
