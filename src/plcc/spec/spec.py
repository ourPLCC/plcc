from .specvalidator import SpecValidator

class Spec:
    def __init__(self, lexspec, bnfspec, semspecs):
        self._lexspec = lexspec
        self._bnfspec = bnfspec
        self._semspecs = semspecs

    def validate(self):
        SpecValidator().validate(self)
