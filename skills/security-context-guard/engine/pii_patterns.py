"""Fixed table of mechanically-detectable PII shapes.

Same discipline as secret_patterns.py: leads, not verdicts, heuristic
regexes with a real false-positive/negative rate (see
project-memory-bank/12-known-limitations.md), and every match is redacted
before it reaches any output surface.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PiiPattern:
    pattern_id: str
    category: str
    regex: re.Pattern[str]
    description: str


PATTERNS: list[PiiPattern] = [
    PiiPattern(
        "email-address", "email",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "Looks like an email address.",
    ),
    PiiPattern(
        "phone-number", "phone",
        re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}\b"),
        "Looks like a phone number.",
    ),
    PiiPattern(
        "ssn-shaped", "ssn",
        re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
        "Looks like a US Social Security Number.",
    ),
    PiiPattern(
        "credit-card-shaped", "credit-card",
        re.compile(r"\b(?:\d[ -]?){13,16}\b"),
        "Looks like a credit-card-shaped digit run.",
    ),
]
