from __future__ import annotations
from dataclasses import dataclass, field

from ..spec.bnfrule import BnfRule


@dataclass(frozen=True)
class Class:
    name: ClassName | StrClassName
    extends: BaseClassName = None
    fields: [FieldDeclaration] = field(default_factory=list)
    constructor: Constructor = None


@dataclass(frozen=True)
class StrClassName:
    name: str


@dataclass(frozen=True)
class FieldDeclaration:
    name: VariableName
    type: TypeName


@dataclass(frozen=True)
class Constructor:
    className: ClassName
    parameters: [Parameter]
    assignments: [AssignVariableToField]


@dataclass(frozen=True)
class Parameter:
    name: VariableName | ListVariableName
    type: TypeName | ListTypeName


@dataclass(frozen=True)
class AssignVariableToField:
    lhs: FieldReference
    rhs: VariableName


@dataclass(frozen=True)
class FieldReference:
    name: VariableName


@dataclass(frozen=True)
class TypeName:
    symbol: Symbol


@dataclass(frozen=True)
class ListTypeName:
    symbol: Symbol


@dataclass(frozen=True)
class VariableName:
    symbol: Symbol


@dataclass(frozen=True)
class ListVariableName:
    symbol: Symbol


@dataclass(frozen=True)
class ClassName:
    symbol: Symbol


@dataclass(frozen=True)
class BaseClassName:
    symbol: Symbol
