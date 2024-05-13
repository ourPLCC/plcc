from dataclasses import dataclass


@dataclass
class Block:
    cls: str
    hook: str
    code: str
    startLine: Line
