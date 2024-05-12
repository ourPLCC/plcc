from dataclasses import dataclass, replace


@dataclass(frozen=True)
class Line:
    path: str = None
    number: int = None
    string: str = None
    isInBlock: bool = False

    def markIsInBlock(self):
        return replace(self, isInBlock=True)

