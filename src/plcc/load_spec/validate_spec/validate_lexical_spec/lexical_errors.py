from dataclasses import dataclass
from ...load_rough_spec.parse_lines import Line


@dataclass
class ValidationError:
    line: Line
    message: str

@dataclass
class InvalidNameFormatError(ValidationError):
    def __init__(self, rule):
        self.line = rule.line
        self.message = f"Invalid name format for rule '{rule.name}' (Must be uppercase letters, numbers, and underscores, and cannot start with a number) on line: {rule.line.number}"

@dataclass
class DuplicateNameError(ValidationError):
    def __init__(self, rule):
        self.line = rule.line
        self.message = f"Duplicate rule name found '{rule.name}' on line: {rule.line.number}"

@dataclass
class InvalidPatternError(ValidationError):
    def __init__(self, rule):
        self.line = rule.line
        self.message = f"Invalid pattern format found '{rule.pattern}' on line: {rule.line.number} (Patterns can not contain closing closing quotes)"

@dataclass
class InvalidRuleError(ValidationError):
    def __init__(self, line):
        self.line = line
        self.message = f"Invalid rule format found on line: {line.number}"
