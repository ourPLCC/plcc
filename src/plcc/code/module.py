from dataclasses import dataclass
from dataclasses import field


from .class_ import Class


@dataclass(frozen=True)
class Module:
    classes: [Class] = field(default_factory=list)
