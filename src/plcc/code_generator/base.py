class CodeGenerator():

    def __init__(self, spec, stubs):
        self._spec = spec.copy() if spec is not None else {}
        self._stubs = stubs.copy() if stubs is not None else {}

    def addCodeToClass(self, cls, mod, code):
        if cls in self._stubs:
            if mod and mod != 'ignore' and mod != 'top':
                code = '\n'.join(indent(2,code))
            else:
                code = '\n'.join(indent(1,code))
        else:
            code = '\n'.join(code)
        if mod:
            if cls == '*': # apply the mod substitution to *all* of the stubs
                for cls in self._stubs:
                    stub = self._stubs[cls]
                    repl = '{}{}:{}{}'.format(self._spec['lineComment'],cls,mod,self._spec['lineComment'])
                    stub = stub.replace(repl, '{}\n{}'.format(code,repl))
                    repl = "{}{}:{}{}".format(self._spec['blockCommentStart'], cls, mod, self._spec['blockCommentEnd'])
                    stub = stub.replace(repl, '{} {}'.format(code,repl))
                    self._stubs[cls] = stub
                return
        if cls in self._stubs:
            stub = self._stubs[cls]
            if mod:
                repl = '{}{}:{}{}'.format(self._spec['lineComment'],cls,mod,self._spec['lineComment'])
                stub = stub.replace(repl, '{}\n{}'.format(code,repl))
                repl = '{}{}:{}{}'.format(self._spec['blockCommentStart'],cls,mod,self._spec['blockCommentEnd'])
                stub = stub.replace(repl, '{} {}'.format(code,repl))
            else: # the default
                repl = '{}{}{}'.format(self._spec['lineComment'],cls,self._spec['lineComment'])
                stub = stub.replace(repl, '{}\n\n{}'.format(code,repl))
            self._stubs[cls] = stub
        else:
            if mod:
                deathLNO('no stub for class {} -- cannot replace {}{}:{}{}'.format(cls,self._spec['lineComment'],cls,mod,self._spec['lineComment']))
            self._stubs[cls] = code

    def addStub(self, cls, fieldVars, startSymbol, lhs, extClass, ruleString, parseString):
        decls = []
        inits = []
        params = []
        for (field, fieldType) in fieldVars:
            decls.append(self._spec['declFormatString'].format(fieldType=fieldType, field=field))
            inits.append(self._spec['initFormatString'].format(field=field))
            params.append(self._spec['paramFormatString'].format(fieldType=fieldType, field=field))
        if cls == nt2cls(startSymbol):
            ext = self._spec['extendFormatString'].format(cls='_Start')
        elif extClass != '':
            ext = self._spec['extendFormatString'].format(cls=extClass)
        else:
            ext = ''
        stubString = self._spec['stubFormatString'].format(cls=cls,
            lhs=lhs,
            ext=ext,
            ruleString=ruleString,
            decls='\n'.join(indent(1,decls)),
            params=', '.join(params),
            inits='\n'.join(indent(2,inits)),
            parse=parseString)
        self._stubs[cls] = stubString

    def getStubs(self):
        return self._stubs.copy()


def indent(n, iList):
    ### make a new list with the old list items prepended with 4*n spaces
    indentString = '    '*n
    newList = []
    for item in iList:
        newList.append('{}{}'.format(indentString, item))
    # print('### str={}'.format(str))
    return newList


def nt2cls(nt):
    # return the class name of the nonterminal nt
    return nt[0].upper() + nt[1:]
