"""Обход файлов и применение правил."""

from pathlib import Path

from src.ignore import parse_ignores
from src.rules import Rule


def find_in_file(path: Path, rules: list[Rule]) -> list[dict]:
    """Найти все срабатывания правил в одном файле."""
    findings: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return findings

    for lineno, line in enumerate(text.splitlines(), start=1):
        ignored = parse_ignores(line)
        for rule in rules:
            if rule.id in ignored:
                continue
            match = rule.compile().search(line)
            if match:
                findings.append(
                    {
                        "rule_id": rule.id,
                        "severity": rule.severity.value,
                        "file": str(path),
                        "line": lineno,
                        "column": match.start() + 1,
                        "message": rule.message,
                    }
                )
    return findings


def scan_directory(root: str, rules: list[Rule]) -> list[dict]:
    """Рекурсивно пройти по *.py и собрать находки."""
    root_path = Path(root)
    findings: list[dict] = []
    for path in root_path.rglob("*.py"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        findings.extend(find_in_file(path, rules))
    return findings
