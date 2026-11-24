"""Юнит-тесты правил и парсера ignore."""

from src.ignore import parse_ignores
from src.rules import DEFAULT_RULES, Severity


def test_parse_noqa():
    assert parse_ignores("x = 1  # noqa: SEC001") == {"SEC001"}


def test_parse_multiple():
    assert parse_ignores("# noqa: SEC001, STY001") == {"SEC001", "STY001"}


def test_default_rules_have_critical_eval():
    ids = [r.id for r in DEFAULT_RULES if r.severity == Severity.CRITICAL]
    assert "SEC001" in ids


def test_eval_matches():
    rule = next(r for r in DEFAULT_RULES if r.id == "SEC001")
    assert rule.compile().search("x = eval('1+1')")
