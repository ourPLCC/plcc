from .bnfvalidator import BnfValidator
from .lexvalidator import LexValidator
from .semvalidator import SemValidator
from .specvalidator import SpecValidator


class SpecValidator:
    def __init__(self):
        self._lexValidator = LexValidator()
        self._bnfValidator = BnfValidator()
        self._semValidator = SemValidator()

    def validate(self, spec):
        self._lexValidator.validate(spec.getLexSpec())
        self._bnfValidator.validate(spec.getBnfSpec())
        for s in spec.getSemSpecs():
            self._semValidator.validate(s)
        self._all_terminals_are_tokens(spec.getLexSpec(), spec.getBnfSpec())

    def _all_terminals_are_tokens(self, lexSpec, bnfSpec):
        ...
