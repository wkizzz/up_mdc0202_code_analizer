"""Правила статического анализа и уровни важности."""

import re
from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    """Уровень важности находки."""

    INFO = "INFO"
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    CRITICAL = "CRITICAL"

    @property
    def rank(self) -> int:
        return {"INFO": 0, "MINOR": 1, "MAJOR": 2, "CRITICAL": 3}[self.value]


@dataclass
class Rule:
    """Правило анализа: регулярка + уровень + сообщение."""

    id: str
    pattern: str
    severity: Severity
    message: str

    def compile(self) -> re.Pattern:
        return re.compile(self.pattern)


DEFAULT_RULES = [
    Rule("SEC001", r"\beval\s*\(", Severity.CRITICAL, "Использование eval() опасно"),
    Rule("SEC002", r"\bexec\s*\(", Severity.CRITICAL, "Использование exec() опасно"),
    Rule("SEC003", r"\bos\.system\s*\(", Severity.MAJOR, "Использование os.system() небезопасно"),
    Rule(
        "SEC004",
        r"subprocess\.[^(]+\([^)]*shell\s*=\s*True",
        Severity.MAJOR,
        "subprocess с shell=True небезопасен",
    ),
    Rule("SEC005", r"\bpickle\.loads\s*\(", Severity.MAJOR, "pickle.loads() небезопасен"),
    Rule("STY001", r"^.{121,}$", Severity.MINOR, "Строка длиннее 120 символов"),
    Rule(
        "TODO1",
        r"#\s*(TODO|FIXME|HACK)\b",
        Severity.INFO,
        "Незавершённая работа (TODO/FIXME/HACK)",
    ),
]
