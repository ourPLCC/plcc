class SyntacticSpec():
    def __init__(self):
        self._rules = None
        self._nonterminals = None
        self._extends = None
        self._derives = None
        self._startSymbol = None
        self._cases = {}   # this was global; might depend on buildStubs which I haven't processed yet.

    def initRules(self, rules):
        self._rules = rules

    def initNonterminals(self, nonterminals):
        self._nonterminals = nonterminals

    def initExtends(self, extends):
        self._extends = extends

    def initDerives(self, derives):
        self._derives = derives

    def initStartSymbol(self, startSymbol):
        self._startSymbol = startSymbol

    def validate(self):
        if not self._rules:
            return
        # check to make sure all RHS nonterms appear as the LHS of at least one rule
        for (nt, cls, rhs) in self._rules:
            rhsString = ''
            for item in rhs:
                if self._isValidNonterm(item):
                    rhsString += f' <{item}>'
                    if not item in self._nonterminals:
                        raise Exception(f'nonterm {item} appears on the RHS of rule "<{nt}> ::= {rhsString} ..." but not on any LHS')
                else:
                    rhsString += f' {item}'

        self._checkLL1()

    def _chekckLL1(self):
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
            if self._isValidTerm(tnt):
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
            return fst

        for nt in self._nonterminals:
            first[nt] = set()        # initialize all of the first sets
            follow[nt] = set()       # initialize all of the follow sets
            switch[nt] = []          # maps each nonterm to a list of its first sets

        # determine the first sets
        modified = True
        while modified:
            modified = False  # assume innocent
            for (nt, cls, rhs) in self._rules:
                fst = first[nt]      # the current first set for this nonterminal
                fct = len(fst)       # see if the first set changes
                fst.update(getFirst(rhs))   # add any new terminals to the set
                if len(fst) != fct:
                    modified = True

        # determine the follow sets
        modified = True
        while modified:
            modified = False
            for (nt, cls, rhs) in self._rules:
                rhs = rhs[:]         # make a copy
                while rhs:
                    tnt = rhs.pop(0) # remove the first element of the list
                    if self._isValidNonterm(tnt):
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

        # determine the switch sets for each nonterm and corresponding rhs
        for (nt, cls, rhs) in self._rules:
            # print('### nt={} cls={} rhs= {}'.format(nt, cls, ' '.join(rhs)))
            fst = getFirst(rhs)
            if 'Null' in fst:
                # the rhs can derive the empty string, so remove Null from the set
                fst -= {'Null'}
                # add all of the terminals in follow[nt] to this switch set
                fst.update(follow[nt])
            switch[nt].append((fst, rhs))
            if cls != None:
                self._saveCases(cls, fst)

        # finally check for LL(1)
        for nt in switch:
            allTerms = set()
            for (fst, rhs) in switch[nt]:
                s = allTerms & fst   # check to see if fst has any tokens already in allTerms
                if s:
                    raise Exception(f'''\
not LL(1):
term(s) {' '.join(fst)} appears in first sets for more than one rule starting with nonterm {nt}
''')
                else:
                    allTerms.update(fst)
            if not allTerms:
                raise Exception(f'possibly useless or left-recursive grammar rule for nonterm {nt}')
            self._cases[nt] = allTerms

    def _saveCases(self, cls, fst):
        if cls in self._cases:
            raise Exception(f'cases for class {cls} already accounted for')
        if cls in self._derives:
            raise Exception(f'{cls} is an abstract class')
        self._cases[cls] = fst

    def __str__(self):
        if not self._rules:
            return 'No grammar rules'
        s = []
        s.append('Nonterminals (* indicates start symbol):')
        for nt in sorted(self._nonterminals):
            if nt[-1] == '#':
                continue  # ignore automatically generated repeating rule names
            if nt == self._startSymbol:
                s.append(f' *<{nt}>')
            else:
                s.append(f'  <{nt}>')
        s.append('')
        s.append('Abstract classes:')
        for cls in sorted(derives):
            s.append(f'  {cls}')
        return s

    def _isValidNonterm(self, nt):
        if nt == 'void' or len(nt) == 0:
            return False
        return re.match(r'[a-z]\w*#?$', nt)
