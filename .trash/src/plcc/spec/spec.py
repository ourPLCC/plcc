from .validator import SpecValidator

class Spec:
    def __init__(self, lexspec, bnfspec, semspecs):
        self.lexspec = lexspec
        self.bnfspec = bnfspec
        self.semspecs = semspecs
