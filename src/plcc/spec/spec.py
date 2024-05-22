from dataclasses import dataclass
from .lexrule import LexRule
from .bnfrule import BnfRule
from .semrule import SemRule


@dataclass(frozen=True)
class Spec:
    lexRules: [LexRule]
    bnfRules: [BnfRule]
    semRules: [[SemRule]]
