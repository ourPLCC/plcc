from __future__ import annotations
from dataclasses import dataclass
from dataclasses import replace

START_TYPE = Type('_Start', isList=False)

@dataclass(frozen=True)
class Class:
    name: ClassName = None
    extends: ClassName = None
    fields: [Variable] = []
    methods: [Method] = []

@dataclass(frozen=True)
class ClassName:
    name: str = None

@dataclass(frozen=True)
class Enum:
    name: ClassName = None
    values: [ConstantName] = []

@dataclass(frozen=True)
class ConstantName:
    name: str = None

@dataclass(frozen=True)
class Variable:
    name: VariableName
    type: Type
    isField: bool
    def toNonField(self):
        return replace(self, isField=False)

@dataclass(frozen=True)
class VariableName:
    germ: str = None
    isList: bool = None

@dataclass(frozen=True)
class Type:
    germ: str = None
    isList: bool = False

@dataclass(frozen=True)
class Method:
    name: MethodName
    returnType: Type
    parameters: [Variable]
    body: [Statement]

@dataclass(frozen=True)
class MethodName:
    name: str = None

@dataclass(frozen=True)
class Type:
    name: str
    isList: bool

@dataclass(frozen=True)
class Statement:
    ...

@dataclass(frozen=True)
class ConstructorAssignmentStatement(Statement):
    lhs: Variable
    rhs: Variable

@dataclass(frozen=True)
class PrintSelfAsStringStatement(Statement):
    pass
