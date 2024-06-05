from __future__ import annotations
from dataclasses import dataclass, field

from ..spec.bnfrule import BnfRule


@dataclass(frozen=True)
class Module:
    classes: [Class] = field(default_factory=list)


@dataclass(frozen=True)
class Class:
    name: UnresolvedClassName | ClassName
    extends: UnresolvedBaseClassName = None
    fields: [FieldDeclaration] = field(default_factory=list)


@dataclass(frozen=True)
class ClassName:
    name: str


@dataclass(frozen=True)
class FieldDeclaration:
    name: UnresolvedVariableName
    type: UnresolvedTypeName


@dataclass(frozen=True)
class UnresolvedTypeName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.isTerminal:
            return language.toTypeName('Token')
        else:
            return language.toTypeName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedVariableName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return language.toVariableName(self.symbol.givenName)
        else:
            return language.toVariableName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedClassName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return language.toClassName(self.symbol.givenName)
        else:
            return language.toClassName(self.symbol.name)


@dataclass(frozen=True)
class UnresolvedBaseClassName:
    symbol: Symbol

    def to(self, language):
        return language.toBaseClassName(self.symbol.name)

