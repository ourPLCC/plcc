import pytest


from plcc.spec.bnfvalidator import BnfValidator
from plcc.spec.bnfrule import BnfRule


@pytest.fixture
def validator():
    return BnfValidator()


def test_(validator):
    ...
