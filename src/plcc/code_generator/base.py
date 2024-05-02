from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def getLineComment(self):
        ...

    @abstractmethod
    def getBlockCommentStart(self):
        ...

    @abstractmethod
    def getBlockCommentEnd(self):
        ...

    @abstractmethod
    def makeFieldDeclaration(self, type, name):
        ...

    @abstractmethod
    def makeFieldInitializer(self, name):
        ...

    @abstractmethod
    def makeParameterDeclaration(self, type, name):
        ...

    @abstractmethod
    def makeExtendsClause(self, type):
        ...

    @abstractmethod
    def makeStub(self, cls, lhs, ext, ruleString, decls, params, inits, parse):
        ...

    @abstractmethod
    def makeAbstractStub(self, cls, base, ext, cases):
        ...


class CodeGenerator(Base):
    def __init__(self, stubs):
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
                    repl = '{}{}:{}{}'.format(self.getLineComment(),cls,mod,self.getLineComment())
                    stub = stub.replace(repl, '{}\n{}'.format(code,repl))
                    repl = "{}{}:{}{}".format(self.getBlockCommentStart(), cls, mod, self.getBlockCommentEnd())
                    stub = stub.replace(repl, '{} {}'.format(code,repl))
                    self._stubs[cls] = stub
                return
        if cls in self._stubs:
            stub = self._stubs[cls]
            if mod:
                repl = '{}{}:{}{}'.format(self.getLineComment(),cls,mod,self.getLineComment())
                stub = stub.replace(repl, '{}\n{}'.format(code,repl))
                repl = '{}{}:{}{}'.format(self.getBlockCommentStart(),cls,mod,self.getBlockCommentEnd())
                stub = stub.replace(repl, '{} {}'.format(code,repl))
            else: # the default
                repl = '{}{}{}'.format(self.getLineComment(),cls,self.getLineComment())
                stub = stub.replace(repl, '{}\n\n{}'.format(code,repl))
            self._stubs[cls] = stub
        else:
            if mod:
                deathLNO('no stub for class {} -- cannot replace {}{}:{}{}'.format(cls,self.getLineComment(),cls,mod,self.getLineComment()))
            self._stubs[cls] = code

    def addStub(self, cls, fieldVars, startSymbol, lhs, extClass, ruleString, parseString):
        decls = []
        inits = []
        params = []
        for (field, fieldType) in fieldVars:
            decls.append(self.makeFieldDeclaration(type=fieldType, name=field))
            inits.append(self.makeFieldInitializer(name=field))
            params.append(self.makeParameterDeclaration(type=fieldType, name=field))
        if cls == nt2cls(startSymbol):
            ext = self.makeExtendsClause('_Start')
        elif extClass != '':
            ext = self.makeExtendsClause(extClass)
        else:
            ext = ''
        decls='\n'.join(indent(1,decls))
        params=', '.join(params)
        inits='\n'.join(indent(2,inits))
        stubString = self.makeStub(cls,lhs,ext,ruleString,decls,params,inits,parseString)
        self._stubs[cls] = stubString

    def addAbstractStub(self, base, derives, cases, startSymbol, caseIndentLevel, ext):
        caseList = []    # a list of strings,
                        # either 'case XXX:'
                        # or '    return Cls.parse(...);'
        for cls in derives[base]:
            for tok in cases[cls]:
                caseList.append('case {}:'.format(tok))
            caseList.append('    return {}.parse(scn$,trace$);'.format(cls))
        if base != nt2cls(startSymbol):
            ext = ''
        cases='\n'.join(indent(caseIndentLevel, caseList))
        stubString = self.makeAbstractStub(cls, base, ext, cases)
        self._stubs[base] = stubString

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
