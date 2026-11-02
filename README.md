# Code Analyzer

[![CI](https://github.com/wkizzz/up_mdc0202_code_analizer/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/wkizzz/up_mdc0202_code_analizer/actions/workflows/ci.yml)

Модуль статического анализа Python-кода в рамках учебной практики УП 02.02,
вариант 9.

## Возможности

- Настраиваемые правила (стандартные + пользовательские через YAML)
- Отчёты в JSON и SARIF для интеграции с IDE
- Блокировка CI при находках уровня CRITICAL
- Inline-игнорирование ложных срабатываний (`# noqa: RULE_ID`)

## Требования

- Python 3.10+
- Зависимости — в `requirements.txt`

## Установка

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Запуск

```bash
python -m src.main --path ./src
python -m src.main --path ./src --format sarif --output report.sarif
```

## Тесты

```bash
pytest --cov=src tests/
```

## Структура

```
up_mdc0202_code_analizer/
├── .github/    — CI, шаблоны PR и Issue
├── docs/       — документация и UML
├── src/        — исходный код
├── tests/      — юнит-тесты
├── pyproject.toml
└── requirements.txt
```

