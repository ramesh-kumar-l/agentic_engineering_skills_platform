"""Applies safety_patterns.py's anti-pattern table to a free-text
refactoring description."""

from __future__ import annotations

from .models import SafetyFlag
from .safety_patterns import ABSENCE_PATTERNS, PATTERNS


def scan(refactor_text: str) -> list[SafetyFlag]:
    flags: list[SafetyFlag] = []

    for pattern in PATTERNS:
        match = pattern.regex.search(refactor_text)
        if not match:
            continue
        flags.append(
            SafetyFlag(
                pattern_id=pattern.pattern_id,
                category=pattern.category,
                severity=pattern.severity,
                description=pattern.description,
                matched_text=match.group(0),
            )
        )

    for absence in ABSENCE_PATTERNS:
        if absence.regex.search(refactor_text):
            continue
        flags.append(
            SafetyFlag(
                pattern_id=absence.pattern_id,
                category=absence.category,
                severity=absence.severity,
                description=absence.description,
                matched_text="",
            )
        )

    return flags
