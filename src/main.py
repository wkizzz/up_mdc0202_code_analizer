"""CLI-точка входа модуля статического анализа."""

import argparse
import sys

from src.config import load_rules
from src.report import save, to_json, to_sarif
from src.rules import Severity
from src.scanner import scan_directory


def build_parser() -> argparse.ArgumentParser:
    """Собрать парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        prog="code-analyzer",
        description="Статический анализ Python-кода",
    )
    parser.add_argument("--path", required=True, help="Папка для анализа")
    parser.add_argument("--config", default=None, help="YAML-конфиг с правилами")
    parser.add_argument("--format", choices=["json", "sarif"], default="json", help="Формат отчёта")
    parser.add_argument("--output", default=None, help="Файл для отчёта")
    parser.add_argument(
        "--fail-on",
        choices=["info", "minor", "major", "critical"],
        default="critical",
        help="Минимальный уровень для exit-code 1",
    )
    return parser


def main() -> int:
    """Точка входа: анализ + отчёт + exit-code."""
    args = build_parser().parse_args()
    rules = load_rules(args.config)
    findings = scan_directory(args.path, rules)

    text = to_sarif(findings) if args.format == "sarif" else to_json(findings)
    if args.output:
        save(text, args.output)
        print(f"Отчёт сохранён: {args.output}")
    else:
        print(text)

    threshold = Severity(args.fail_on.upper()).rank
    worst = max((Severity(f["severity"]).rank for f in findings), default=-1)
    return 1 if findings and worst >= threshold else 0


if __name__ == "__main__":
    sys.exit(main())
