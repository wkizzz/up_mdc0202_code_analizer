"""Загрузка конфигурации правил из YAML или встроенного набора."""

from pathlib import Path

import yaml

from src.rules import DEFAULT_RULES, Rule, Severity


def load_rules(config_path: str | None) -> list[Rule]:
    """Вернуть список правил: встроенные + пользовательские из конфига."""
    if not config_path:
        return list(DEFAULT_RULES)

    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Конфиг не найден: {config_path}")

    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rules = list(DEFAULT_RULES)

    for item in data.get("rules", []):
        rules.append(
            Rule(
                id=item["id"],
                pattern=item["pattern"],
                severity=Severity(item.get("severity", "MINOR").upper()),
                message=item.get("message", ""),
            )
        )
    return rules
