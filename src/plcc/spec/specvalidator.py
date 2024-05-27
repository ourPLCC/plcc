
class SpecValidator:
    def validate(self, spec):
        lexSpec = spec.getLexSpec()
        bnfSpec = spec.getBnfSpec()
        semSpecs = spec.getSemSpecs()

        self._validateLexSpec(lexSpec)
        self._validateBnfSpec(bnfSpec, lexSpec, semSpecs)
        for semSpec in spec.getSemSpecs():
            self._validateSemSpec.validate(semSpec, bnfSpec)

    def _validateLexSpec(self, lexSpec):
        lexSpec.validate()

    def _validateBnfSpec(self, bnfSpec, lexSpec, semSpecs):
        bnfSpec.validate()
        bnfSpec.validateAgainstLexSpec(lexSpec)
        for semSpec in semSpecs:
            semSpec.validateAgainstSemSpec(semSpec)

    def _validateSemSpec(self, semSpec, bnfSpec):
        semSpec.validate()
        semSpec.validateAgainstBnfSpec(bnfSpec)

