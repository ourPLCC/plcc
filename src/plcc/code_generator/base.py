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

    def addCodeToClass(self, cls, hook, code):
        code = self._indentCode(cls, hook, code)
        if self._shouldApplyToAllStubs(cls, hook):
            self._insertIntoAllStubs(hook, code)
        elif self._stubExists(cls):
            self._insertIntoExistingStub(cls, hook, code)
        elif hook:
            raise StubDoesNotExistForHookException(self._makeLineCommentInsertionHook(cls, hook))
        else:
            self._createStub(cls, code)

    def _indentCode(self, cls, hook, code):
        if self._stubExists(cls):
            if hook and hook != 'ignore' and hook != 'top':
                return '\n'.join(indent(2,code))
            else:
                return '\n'.join(indent(1,code))
        else:
            return '\n'.join(code)

    def _shouldApplyToAllStubs(self, cls, hook):
        return hook and cls == '*'

    def _insertIntoAllStubs(self, hook, code):
        for cls in self._stubs:
            self._insertCodeIntoHook(cls, hook, code)

    def _stubExists(self, cls):
        return cls in self._stubs

    def _insertIntoExistingStub(self, cls, hook, code):
        if hook:
            self._insertCodeIntoHook(cls, hook, code)
        else:
            self._insertCodeIntoDefaultHook(cls, code)

    def _createStub(self, cls, code):
        self._stubs[cls] = code

    def _insertCodeIntoHook(self, cls, hook, code):
        repl = self._makeLineCommentInsertionHook(cls, hook)
        self._stubs[cls] = self._stubs[cls].replace(repl, '{}\n{}'.format(code,repl))
        repl = self._makeBlockCommentInsertionHook(cls, hook)
        self._stubs[cls] = self._stubs[cls].replace(repl, '{} {}'.format(code,repl))

    def _insertCodeIntoDefaultHook(self, cls, code):
        repl = self._makeDefaultLineCommentInsertionHook(cls)
        self._stubs[cls] = self._stubs[cls].replace(repl, '{}\n\n{}'.format(code,repl))

    def _makeLineCommentInsertionHook(self, cls, hook):
        return '{}{}:{}{}'.format(self.getLineComment(),cls,hook,self.getLineComment())

    def _makeBlockCommentInsertionHook(self, cls, hook):
        return "{}{}:{}{}".format(self.getBlockCommentStart(), cls, hook, self.getBlockCommentEnd())

    def _makeDefaultLineCommentInsertionHook(self, cls):
        return '{}{}{}'.format(self.getLineComment(),cls,self.getLineComment())

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


class StubDoesNotExistForHookException(Exception):
    pass
