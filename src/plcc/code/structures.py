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
    constructor: Constructor = None


@dataclass(frozen=True)
class StrClassName:
    name: str


@dataclass(frozen=True)
class FieldDeclaration:
    name: UnresolvedVariableName
    type: UnresolvedTypeName

    def to(self, language):
        name = self.name.to(language)
        type = self.type.to(language)
        return language.toFieldDeclaration(name=name, type=type)


@dataclass(frozen=True)
class Constructor:
    className: UnresolvedClassName
    parameters: [Parameter]
    assignments: [AssignVariableToField]

    def to(self, language):
        className = self.className.to(language)
        params = [p.to(language) for p in self.parameters]
        body = [a.to(language) for a in self.assignments]
        return language.toConstructor(className, params, body)


@dataclass(frozen=True)
class Parameter:
    name: UnresolvedVariableName | UnresolvedListVariableName
    type: UnresolvedTypeName | UnresolvedListTypeName

    def to(self, language):
        name = self.name.to(language)
        type = self.type.to(language)
        return language.toParameter(name=name, type=type)


@dataclass(frozen=True)
class AssignVariableToField:
    lhs: FieldReference
    rhs: UnresolvedVariableName

    def to(self, language):
        field = self.lhs.to(language)
        parameter = self.rhs.to(language)
        return language.toAssignmentStatement(field, parameter)


@dataclass(frozen=True)
class FieldReference:
    name: UnresolvedVariableName

    def to(self, language):
        name = self.name.to(language)
        return language.toFieldReference(name)


@dataclass(frozen=True)
class TypeName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.isTerminal:
            return language.toTypeName('Token')
        else:
            return language.toTypeName(self.symbol.name)


@dataclass(frozen=True)
class ListTypeName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.isTerminal:
            return language.toListTypeName('Token')
        else:
            elementTypeName = TypeName(self.symbol).to(language)
            return language.toListTypeName(elementTypeName)


@dataclass(frozen=True)
class VariableName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.toVariableName(self.symbol.name)


@dataclass(frozen=True)
class ListVariableName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.toListVariableName(self.symbol.name)


@dataclass(frozen=True)
class ClassName:
    symbol: Symbol

    def to(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.toClassName(self.symbol.name)


@dataclass(frozen=True)
class BaseClassName:
    symbol: Symbol

    def to(self, language):
        return language.toBaseClassName(self.symbol.name)



