import pytest


from plcc.spec.lexvalidator import LexValidator
from plcc.spec.lexrule import LexRule


@pytest.fixture
def validator():
    return LexValidator()


def makeLexRule(name):
    return LexRule(line=None, name=name, pattern='', quote='', end='', isToken=None)

def test_detects_duplicates(validator):
    rules = [
        makeLexRule('BOB'),
        makeLexRule('BOB'),
    ]
    with pytest.raises(LexValidator.DuplicateName):
        validator.validate(rules)

def test_detects_invalid_names(validator):
    rules = [
        makeLexRule('bOB'),
    ]
    with pytest.raises(LexValidator.InvalidName):
        validator.validate(rules)


def test_empty_rules_are_vacuously_valid(validator):
    validator.validate([])

