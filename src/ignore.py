"""Парсинг inline-директив игнорирования."""

import re

NOQA = re.compile(r"#\s*noqa:\s*([A-Z0-9, ]+)", re.IGNORECASE)
DISABLE = re.compile(r"#\s*analyzer:\s*disable=([A-Z0-9, ]+)", re.IGNORECASE)


def parse_ignores(line: str) -> set[str]:
    """Вернуть множество ID правил, подавлённых в этой строке."""
    result: set[str] = set()
    for pattern in (NOQA, DISABLE):
        match = pattern.search(line)
        if not match:
            continue
        for rule_id in match.group(1).split(","):
            rule_id = rule_id.strip().upper()
            if rule_id:
                result.add(rule_id)
    return result
