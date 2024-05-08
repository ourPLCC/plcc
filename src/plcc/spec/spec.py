class Specification:
    def __init__(self, lexicalSpec, syntacticSpec, semanticSpecInJava, semanticSpecInPython):
        self._lexicalSpecification = lexicalSpec
        self._syntacticSpecification = syntacticSpec
        self._semanticSpecificationInJava = semanticSpecInJava
        self._semanticSpecificationInPython = semanticSpecInPython

    def getTermSpecification(self):
        return self._lexicalSpecification.getTermSpecifications()
