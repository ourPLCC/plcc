from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Class:
    name: Name = None
    extends: Name = None
    fields: [Variable] = []
    methods: [Method] = []
    comment: [str] = None

@dataclass
class Variable:
    name: Name
    type: Type

@dataclass
class Method:
    name: Name
    returnType: Type
    parameters: [Variable]
    body: [str]
    comment: [str]

@dataclass
class Name:
    name: str
    isList: bool
    isFinal: bool

@dataclass
class Type:
    name: str
    isList: bool    # if isList, then name is the element type

START_TYPE = Type('$Start', isList=False)
