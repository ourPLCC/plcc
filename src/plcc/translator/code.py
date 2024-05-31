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
        if self.symbol.alt:
            return language.toVariableName(self.symbol.alt)
        else:
            return language.toVariableName(self.symbol.name)


@dataclass
class UnresolvedClassName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.alt:
            return language.toClassName(self.symbol.alt)
        else:
            return language.toClassName(self.symbol.name)


@dataclass
class UnresolvedBaseClassName:
    symbol: Symbol

    def to(self, language):
        return language.toBaseClassName(self.symbol.name)
