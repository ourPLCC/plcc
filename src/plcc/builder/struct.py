from __future__ import annotations
from dataclasses import dataclass
from dataclasses import replace

@dataclass(frozen=True)
class Class:
    name: Name = None
    extends: Name = None
    fields: [Variable] = []
    methods: [Method] = []

@dataclass(frozen=True)
class Variable:
    name: Name
    type: Type
    isField: bool

    def toNonField(self):
        return replace(self, isField=False)

@dataclass(frozen=True)
class Method:
    name: Name
    returnType: Type
    parameters: [Variable]
    body: [str]

@dataclass(frozen=True)
class Name:
    name: str
    isList: bool
    isFinal: bool

@dataclass(frozen=True)
class Type:
    name: str
    isList: bool    # name is the element type if isList is true

START_TYPE = Type('_Start', isList=False)

@dataclass(frozen=True)
class ConstructorAssignmentStatement:
    lhs: Variable
    rhs: Variable
