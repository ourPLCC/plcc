
from dataclasses import dataclass


from .line import Line


@dataclass(frozen=True)
class SemRule:
    class_: str
    modifier: str
    code: [Line]
