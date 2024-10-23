from dataclasses import dataclass
from ...load_rough_spec.parse_lines import Line, parse_lines
from ...parse_spec.parse_semantic_spec import SemanticSpec, CodeFragment
import re

@dataclass
class InvalidClassNameError:
    line: Line
    message: str

def validate_semantic_spec(semanticSpec: SemanticSpec):
    return SemanticValidator(semanticSpec).validate()

class SemanticValidator:
    def __init__(self, semanticSpec: SemanticSpec):
        self.semanticSpec = semanticSpec
        self.errorList = []

    def validate(self) -> list:
        if (len(self.semanticSpec.codeFragmentList) == 0):
            return self.errorList

        for codeFragment in self.semanticSpec.codeFragmentList:
            self._checkTargetLocatorClassName(codeFragment)

        return self.errorList

    def _checkTargetLocatorClassName(self, codeFragment: CodeFragment):
        if not re.match(r'^[A-Z][A-Za-z0-9_]*$', codeFragment.targetLocator.className):
            self.errorList.append(InvalidClassNameError(codeFragment.targetLocator.line,
            f"Invalid name format for ClassName {codeFragment.targetLocator.className}, (Must start with an upper case letter, and may contain upper or lower case letters, numbers, and underscores)."))






