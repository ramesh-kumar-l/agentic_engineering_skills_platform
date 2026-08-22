"""Applies patterns.py's testability anti-pattern table to a RequirementContext."""

from __future__ import annotations

from .models import RequirementContext, TestabilityFlag
from .patterns import ABSENCE_PATTERNS, PATTERNS


def scan(context: RequirementContext) -> list[TestabilityFlag]:
    flags: list[TestabilityFlag] = []

    for sentence in context.sentences:
        for pattern in PATTERNS:
            match = pattern.regex.search(sentence.text)
            if not match:
                continue
            flags.append(
                TestabilityFlag(
                    pattern_id=pattern.pattern_id,
                    category=pattern.category,
                    severity=pattern.severity,
                    sentence_index=sentence.index,
                    description=pattern.description,
                    matched_text=match.group(0),
                )
            )

    for absence in ABSENCE_PATTERNS:
        if absence.regex.search(context.raw_text):
            continue
        flags.append(
            TestabilityFlag(
                pattern_id=absence.pattern_id,
                category=absence.category,
                severity=absence.severity,
                sentence_index=None,
                description=absence.description,
                matched_text="",
            )
        )

    return flags
