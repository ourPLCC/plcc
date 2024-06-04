from dataclasses import dataclass


from .names import UnresolvedClassName
from .names import UnresolvedBaseClassName
from .names import ClassName


@dataclass(frozen=True)
class Class:
    name: UnresolvedClassName
    extends: ClassName | UnresolvedBaseClassName = None
