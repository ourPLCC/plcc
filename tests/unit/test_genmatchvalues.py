
from plcc.java_frontend.genmatchvalue import genMatchValue


def assertRuleGeneratesValue(rule, value):
    assert genMatchValue(rule) == value


def test_skips():
    assertRuleGeneratesValue(r"skip WS '\s+'", r'WS ("\\s+", TokType.SKIP)')


def test_explicit_token_rule():
    assertRuleGeneratesValue(r"token NUM '\d+'", r'NUM ("\\d+")')


def test_implicit_token_rule():
    assertRuleGeneratesValue(r"token NUM '\d+'", r'NUM ("\\d+")')
