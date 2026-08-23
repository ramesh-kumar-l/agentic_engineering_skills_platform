"""Applies decision_patterns.py's anti-pattern table to a free-text
architecture-decision description."""

from __future__ import annotations

from .decision_patterns import ABSENCE_PATTERNS, PATTERNS
from .models import DecisionFlag


def scan(decision_text: str) -> list[DecisionFlag]:
    flags: list[DecisionFlag] = []

    for pattern in PATTERNS:
        match = pattern.regex.search(decision_text)
        if not match:
            continue
        flags.append(
            DecisionFlag(
                pattern_id=pattern.pattern_id,
                category=pattern.category,
                severity=pattern.severity,
                description=pattern.description,
                matched_text=match.group(0),
            )
        )

    for absence in ABSENCE_PATTERNS:
        if absence.regex.search(decision_text):
            continue
        flags.append(
            DecisionFlag(
                pattern_id=absence.pattern_id,
                category=absence.category,
                severity=absence.severity,
                description=absence.description,
                matched_text="",
            )
        )

    return flags
