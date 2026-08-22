"""Applies planning_patterns.py's anti-pattern table to a free-text task
description."""

from __future__ import annotations

from .models import PlanningFlag
from .planning_patterns import ABSENCE_PATTERNS, PATTERNS


def scan(task_text: str) -> list[PlanningFlag]:
    flags: list[PlanningFlag] = []

    for pattern in PATTERNS:
        match = pattern.regex.search(task_text)
        if not match:
            continue
        flags.append(
            PlanningFlag(
                pattern_id=pattern.pattern_id,
                category=pattern.category,
                severity=pattern.severity,
                description=pattern.description,
                matched_text=match.group(0),
            )
        )

    for absence in ABSENCE_PATTERNS:
        if absence.regex.search(task_text):
            continue
        flags.append(
            PlanningFlag(
                pattern_id=absence.pattern_id,
                category=absence.category,
                severity=absence.severity,
                description=absence.description,
                matched_text="",
            )
        )

    return flags
