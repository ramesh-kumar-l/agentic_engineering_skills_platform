"""Applies symptom_patterns.py's anti-pattern table to a free-text symptom
description."""

from __future__ import annotations

from .models import SymptomFlag
from .symptom_patterns import ABSENCE_PATTERNS, PATTERNS


def scan(symptom_text: str) -> list[SymptomFlag]:
    flags: list[SymptomFlag] = []

    for pattern in PATTERNS:
        match = pattern.regex.search(symptom_text)
        if not match:
            continue
        flags.append(
            SymptomFlag(
                pattern_id=pattern.pattern_id,
                category=pattern.category,
                severity=pattern.severity,
                description=pattern.description,
                matched_text=match.group(0),
            )
        )

    for absence in ABSENCE_PATTERNS:
        if absence.regex.search(symptom_text):
            continue
        flags.append(
            SymptomFlag(
                pattern_id=absence.pattern_id,
                category=absence.category,
                severity=absence.severity,
                description=absence.description,
                matched_text="",
            )
        )

    return flags
