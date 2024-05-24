import pytest


from plcc.spec.specreader import SpecReader
from plcc.spec.bnfspec import BnfSpec
from plcc.spec.bnfparser import BnfParser
from plcc.spec.bnfvalidator import BnfValidator


def toSpec(string):
    reader = SpecReader()
    parser = BnfParser()
    lines = reader.readLinesFromString(string)
    spec = parser.parseBnfSpec(lines)
    return spec


@pytest.fixture
def validator():
    return BnfValidator()


def test_detects_invalid_terminal_names(validator):
    spec = toSpec(
        '<hi> ::= MOm\n'
    )
    with pytest.raises(BnfValidator.InvalidTerminalName):
        validator.validate(spec)


def test_detects_duplicate_alts_in_LHS(validator):
    spec = toSpec(
        '<hi>One ::= <bye>\n'
        '<bye>One ::= MOM\n'
    )
    with pytest.raises(BnfValidator.DuplicateConcreteClassNameInLhs):
        validator.validate(spec)


def test_duplicate_LHS_nonterminals_must_have_an_alt(validator):
    spec = toSpec(
        '<hi>One ::= DAD\n'
        '<hi> ::= MOM\n'
    )
    with pytest.raises(BnfValidator.DuplicateLhsMustProvideConcreteClassName):
        validator.validate(spec)


def test_alts_unique_within_RHS(validator):
    spec = toSpec(
        '<hi> ::= <DAD>one <MOM>one\n'
    )
    with pytest.raises(BnfValidator.FieldNamesMustBeUniqueWithinRule):
        validator.validate(spec)


def test_duplicate_capturing_RHS_must_have_alt(validator):
    spec = toSpec(
        '<hi> ::= <DAD>one <DAD> <DAD>\n'
    )
    with pytest.raises(BnfValidator.SymbolNeedsFieldName):
        validator.validate(spec)


def test_duplicate_capturing_RHS_must_have_alt_except_one(validator):
    spec = toSpec(
        '<hi> ::= <DAD>one <DAD>two <DAD>\n'
    )
    validator.validate(spec)
    assert True


def test_only_repeating_rules_have_separators(validator):
    spec = toSpec(
        '<hi> ::= MOM +SEP\n'
    )
    with pytest.raises(BnfValidator.NonRepeatingRulesCannotHaveSeparators):
        validator.validate(spec)


def test_separators_must_be_non_capturing(validator):
    spec = toSpec(
        '<hi> **= MOM +<SEP>\n'
    )
    with pytest.raises(BnfValidator.SeparatorMustBeNonCapturing):
        validator.validate(spec)


def test_can_pass_separators_must_be_non_capturing(validator):
    spec = toSpec(
        '<hi> **= MOM +SEP\n'
    )
    validator.validate(spec)
    assert True


def test_each_nonterminal_appears_in_LHS(validator):
    spec = toSpec(
        '<hi> **= MOM <bye>\n'
    )
    with pytest.raises(BnfValidator.NonterminalMustAppearOnLHS):
        validator.validate(spec)


def test_can_pass_each_nonterminal_appears_in_LHS(validator):
    spec = toSpec(
        '<hi> **= MOM <bye>\n'
        '<bye> ::= DAD\n'
    )
    validator.validate(spec)
    assert True


def test_no_errors(validator):
    spec = toSpec(
        '<hi>:Greet ::= <mom>parent AND <dad>:other'
        '<mom>NoSpouse ::='
        '<mom>Spouse ::= SPOUSE <hi>'
        '<dad> ::= DAD'
    )
    validator.validate(spec)
    assert True
