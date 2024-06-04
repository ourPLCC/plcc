
class SpecValidator:
    def __init__(self, lexValidator, bnfValidator, semValidator, translators=None):
        self.lexValidator = lexValidator
        self.bnfValidator = bnfValidator
        self.semValidator = semValidator
        self.codes = translators

    def validate(self, spec):
        self.lexValidator.validate(spec.lexspec)
        self.bnfValidator.validate(spec.bnfspec, spec.lexspec.getTokenNames())
        for semspec in spec.semspecs:
            self.semValidator.validate(semspec)
        for semspec in spec.semspecs:
            translator = self.codes[langs.append(semspec.language)]
            self.bnfValidator.validateForLanguage(spec.bnfspec, translator)
