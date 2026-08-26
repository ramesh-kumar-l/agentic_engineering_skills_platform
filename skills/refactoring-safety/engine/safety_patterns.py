"""Fixed table of mechanically-detectable safety-quality anti-patterns in a
free-text refactoring description.

Mirrors architecture-decision's decision_patterns.py (project-memory-bank/
11-decisions.md ADR-007, reused a seventh time here): these flag *candidates
for an under-specified refactor plan*, not verdicts — a regex cannot know if
a rollback plan is actually adequate, only whether the text exhibits wording
shapes correlated with a refactor described without one. The agent's Step 3
walk against the Refactoring Safety Checklist (project-memory-bank/
05-evaluation-framework.md) is what actually judges plan quality.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SafetyPattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


# Whole-text patterns: matched anywhere in the refactor description.
PATTERNS: list[SafetyPattern] = [
    SafetyPattern(
        "vague-refactor-language", "vague-refactor", "medium",
        re.compile(r"(?i)\b(just|simply|quick|trivial(?:ly)?|straightforward|"
                   r"shouldn'?t break anything|easy|no big deal)\b"),
        "Confidence language with no supporting evidence — a refactor "
        "description that asserts it's safe instead of showing why it's "
        "safe gives the checklist walk nothing concrete to verify.",
    ),
]


# Whole-document absence checks: flagged when the pattern does NOT appear
# anywhere in the refactor description.
@dataclass(frozen=True)
class AbsencePattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


ABSENCE_PATTERNS: list[AbsencePattern] = [
    AbsencePattern(
        "no-test-plan-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(test|tests|testing|coverage|pytest|unit test)\b"),
        "Refactor text never mentions tests or coverage — the checklist's "
        "verification category will have to be stated as an assumption "
        "rather than derived from the plan itself.",
    ),
    AbsencePattern(
        "no-rollback-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(revert|rollback|roll back|feature flag|undo|"
                   r"reversible|two-way door)\b"),
        "Refactor text never addresses how to back out if something breaks "
        "— a refactor with no stated rollback path is riskier than one that "
        "states it has none, because the absence hasn't been considered.",
    ),
    AbsencePattern(
        "no-caller-update-signal", "unstated-signal", "medium",
        re.compile(r"(?i)\b(caller|call site|call sites|usage|usages|"
                   r"reference|references|update all|every call)\b"),
        "Refactor text never mentions updating callers or call sites — for "
        "an operation that changes a public boundary, this is exactly the "
        "step most likely to be forgotten.",
    ),
    AbsencePattern(
        "no-verification-signal", "unstated-signal", "medium",
        re.compile(r"(?i)\b(verify|validate|confirm|regression|CI|"
                   r"continuous integration|smoke test)\b"),
        "Refactor text never states how success will be verified after the "
        "change lands — a refactor plan with no verification step "
        "described is one where 'done' is undefined.",
    ),
]
