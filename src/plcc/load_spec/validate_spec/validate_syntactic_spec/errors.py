from dataclasses import dataclass


@dataclass
class ValidationError:
    def __init__(self, rule):
        self.rule = rule


@dataclass
class InvalidLhsNameError(ValidationError):
    def __init__(self, rule):
        super().__init__(rule)
        self.message = f"Invalid LHS name format for rule: '{
            rule.line.string}' (must start with a lower-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"


@dataclass
class InvalidLhsAltNameError(ValidationError):
    def __init__(self, rule):
        super().__init__(rule)
        self.message = f"Invalid LHS alternate name format for rule: '{
            rule.line.string}' (must start with a upper-case letter, and may contain upper or lower case letters, numbers and/or underscore) on line: {rule.line.number}"


@dataclass
class DuplicateLhsError(ValidationError):
    def __init__(self, rule):
        super().__init__(rule)
        self.message = f"Duplicate lhs name: '{
                rule.line.string}' on line: {rule.line.number}"
