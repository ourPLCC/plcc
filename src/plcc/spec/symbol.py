from dataclasses import dataclass

@dataclass(frozen=True)
class Symbol:
    name: str
    givenName: str
    isCapture: bool
    isTerminal: bool = False
