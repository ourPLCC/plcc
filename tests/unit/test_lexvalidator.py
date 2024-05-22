import pytest


from plcc.spec.lexvalidator import LexValidator
from plcc.spec.lexrule import LexRule


@pytest.fixture
def validator():
    return LexValidator()


def test_detects_duplicates(validator):
    rules = [
        LexRule(type='', name='BOB', pattern='', quote='', end='', line=None),
        LexRule(type='', name='BOB', pattern='', quote='', end='', line=None),
    ]
    with pytest.raises(LexValidator.DuplicateName):
        validator.validate(rules)


def test_detects_invalid_names(validator):
    rules = [
        LexRule(type='', name='bOB', pattern='', quote='', end='', line=None),
    ]
    with pytest.raises(LexValidator.InvalidName):
        validator.validate(rules)


def test_empty_rules_are_vacuously_valid(validator):
    validator.validate([])

