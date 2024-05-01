class CodeGenerator():

    def __init__(self, spec, stubs):
        self._spec = spec.copy()
        self._stubs = stubs.copy()

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
