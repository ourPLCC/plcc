from dataclasses import dataclass


from plcc.spec.bnfrule import Symbol


@dataclass
class UnresolvedTypeName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.isTerminal:
            return language.toTypeName('Token')
        else:
            return language.toTypeName(self.symbol.name)


@dataclass
class UnresolvedVariableName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return language.toVariableName(self.symbol.givenName)
        else:
            return language.toVariableName(self.symbol.name)


@dataclass
class UnresolvedClassName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return language.toClassName(self.symbol.givenName)
        else:
            return language.toClassName(self.symbol.name)


@dataclass
class UnresolvedBaseClassName:
    symbol: Symbol

    def to(self, language):
        return language.toBaseClassName(self.symbol.name)
