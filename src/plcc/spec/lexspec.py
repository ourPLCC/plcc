from .lexvalidator import LexValidator


class LexSpec:
    def __init__(self, lexrules):
        self._rules = lexrules

    def validate(self):
        LexValidator().validate(self)
