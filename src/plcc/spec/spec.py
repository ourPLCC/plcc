class Spec:
    def __init__(self, lexicalSpec, syntacticSpec, semanticSpecs):
        self._lexicalSpec = lexicalSpec
        self._syntacticSpec = syntacticSpec
        self._semanticSpecs = semanticSpecs

    def getTermSpecs(self):
        return self._lexicalSpec.getTermSpecs()
