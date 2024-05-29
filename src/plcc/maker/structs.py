from __future__ import annotations
from dataclasses import dataclass

@dataclass
class File:
    name: str = None
    imports: [str] = []
    class_: Class
    comment: str = None

@dataclass
class Class:
    name: str = None
    extends: str = None
    fields: [Variable] = []
    methods: [Method] = []
    comment: str = None

@dataclass
class Variable:
    name: str = None
    type: str = None

@dataclass
class Method:
    name: str = None
    returnType: str = None
    parameters: [Variable] = []
    body: str = None
    comment: str = None
