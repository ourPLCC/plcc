from .semvalidator import SemValidator


class SemSpec:
    def __init__(self, bnfrules, language):
        self._rules = bnfrules
        self._language = language

    def validate(self):
        SemValidator().validate(self)
