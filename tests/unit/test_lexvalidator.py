import pytest


from plcc.spec.lexvalidator import LexValidator
from plcc.spec.lexrule import LexRule


@pytest.fixture
def validator():
    return LexValidator()


def makeLexRule(name, remainder=''):
    return LexRule(line=None, name=name, pattern='', remainder=remainder, isToken=None)


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
    assert True


def test_detect_unmatched_content(validator):
    rules = [
        makeLexRule('BOB', remainder=' junk')
    ]
    with pytest.raises(LexValidator.UnmatchedContent):
        validator.validate(rules)


def test_but_comments_are_ok(validator):
    rules = [
        makeLexRule('BOB', remainder='   # junk')
    ]
    validator.validate(rules)
    assert True
