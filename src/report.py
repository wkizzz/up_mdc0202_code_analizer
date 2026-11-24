"""Формирование отчётов в JSON и SARIF."""

import json
from pathlib import Path


def to_json(findings: list[dict]) -> str:
    """Сериализовать находки в JSON."""
    return json.dumps(findings, ensure_ascii=False, indent=2)


def to_sarif(findings: list[dict]) -> str:
    """Сериализовать находки в SARIF 2.1.0."""
    results = []
    for finding in findings:
        level = "error" if finding["severity"] == "CRITICAL" else finding["severity"].lower()
        results.append(
            {
                "ruleId": finding["rule_id"],
                "level": level,
                "message": {"text": finding["message"]},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": finding["file"]},
                            "region": {
                                "startLine": finding["line"],
                                "startColumn": finding["column"],
                            },
                        }
                    }
                ],
            }
        )

    sarif = {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {"driver": {"name": "code-analyzer", "version": "0.1.0"}},
                "results": results,
            }
        ],
    }
    return json.dumps(sarif, ensure_ascii=False, indent=2)


def save(text: str, output: str) -> None:
    """Сохранить отчёт в файл."""
    Path(output).write_text(text, encoding="utf-8")
