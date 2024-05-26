from .bnfvalidator import BnfValidator
from .lexvalidator import LexValidator


class Spec:
    def __init__(self, lexspec, bnfspec, semspecs):
        self._lexspec = lexspec
        self._bnfspec = bnfspec
        self._semspecs = semspecs

    def validate(self):
        LexValidator().validate(self._lexspec)
        BnfValidator().validate(self._bnfspec)
        for s in self._semspecs:
            SemValidator().validate(s)
