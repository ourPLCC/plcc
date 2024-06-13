from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    name: str
    givenName: str = ''
    isCapture: bool = True
    isTerminal: bool = False

    def getTypeName(self, tokenClassName='Token'):
        '''
        Return the type of the variable that this RHS symbol defines.
        Note: The list type is language specific and must be constructed
        using this symbol's type as the type of the element in the list.
        '''
        if self.isTerminal:
            return tokenClassName
        else:
            return self.name.capitalize()

    def getVariableName(self):
        '''
        Return the variable name that this RHS symbol defines.
        '''
        if self.givenName:
            return self.givenName
        else:
            return self.name

    def getListVariableName(self):
        '''
        Return the list variable name that this RHS symbol defines.
        '''
        if self.givenName:
            return self.givenName
        else:
            return f'{self.getVariableName()}List'

    def getClassName(self):
        '''
        Return the name of the class that this LHS symbol defines.
        '''
        if self.givenName:
            return self.givenName
        else:
            return self.name.capitalize()

    def getBaseClassName(self):
        '''
        Return the name of the abstract base class from which this LHS
        symbol's class derives.
        '''
        return self.name.capitalize()
