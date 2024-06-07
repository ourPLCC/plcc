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

    def renderWith(self, language):
        return self.name


@dataclass(frozen=True)
class FieldDeclaration:
    name: UnresolvedVariableName
    type: UnresolvedTypeName

    def renderWith(self, language):
        name = self.name.renderWith(language)
        type = self.type.renderWith(language)
        return language.renderFieldDeclaration(name=name, type=type)


@dataclass(frozen=True)
class Constructor:
    className: UnresolvedClassName
    parameters: [Parameter]
    assignments: [AssignVariableToField]

    def renderWith(self, language):
        className = self.className.renderWith(language)
        params = [p.renderWith(language) for p in self.parameters]
        body = [a.renderWith(language) for a in self.assignments]
        return language.renderConstructor(className, params, body)


@dataclass(frozen=True)
class Parameter:
    name: UnresolvedVariableName | UnresolvedListVariableName
    type: UnresolvedTypeName | UnresolvedListTypeName

    def renderWith(self, language):
        name = self.name.renderWith(language)
        type = self.type.renderWith(language)
        return language.renderParameter(name=name, type=type)


@dataclass(frozen=True)
class AssignVariableToField:
    lhs: FieldReference
    rhs: UnresolvedVariableName

    def renderWith(self, language):
        field = self.lhs.renderWith(language)
        parameter = self.rhs.renderWith(language)
        return language.renderAssignmentStatement(field, parameter)


@dataclass(frozen=True)
class FieldReference:
    name: UnresolvedVariableName

    def renderWith(self, language):
        name = self.name.renderWith(language)
        return language.renderFieldReference(name)


@dataclass(frozen=True)
class TypeName:
    symbol: Symbol

    def renderWith(self, language):
        if self.symbol.isTerminal:
            return language.renderTypeName('Token')
        else:
            return language.renderTypeName(self.symbol.name)


@dataclass(frozen=True)
class ListTypeName:
    symbol: Symbol

    def renderWith(self, language):
        if self.symbol.isTerminal:
            return language.renderListTypeName('Token')
        else:
            elementTypeName = TypeName(self.symbol).renderWith(language)
            return language.renderListTypeName(elementTypeName)


@dataclass(frozen=True)
class VariableName:
    symbol: Symbol

    def renderWith(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.renderVariableName(self.symbol.name)


@dataclass(frozen=True)
class ListVariableName:
    symbol: Symbol

    def renderWith(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.renderListVariableName(self.symbol.name)


@dataclass(frozen=True)
class ClassName:
    symbol: Symbol

    def renderWith(self, language):
        if self.symbol.givenName:
            return self.symbol.givenName
        else:
            return language.renderClassName(self.symbol.name)


@dataclass(frozen=True)
class BaseClassName:
    symbol: Symbol

    def renderWith(self, language):
        return language.renderBaseClassName(self.symbol.name)



