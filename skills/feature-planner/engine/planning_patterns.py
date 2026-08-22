"""Fixed table of mechanically-detectable planning anti-patterns in a
free-text task description.

Mirrors acceptance-test-engineer's testability anti-pattern table
(project-memory-bank/11-decisions.md ADR-007, reused a third time here):
these flag *candidates for an under-specified task*, not verdicts — a regex
cannot know if a plan will be good, only whether the task description
exhibits wording shapes that correlate with vague scope. The agent's Step 3
structured-plan derivation (against the Plan Quality checklist in
project-memory-bank/05-evaluation-framework.md) is what actually defines
the plan.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class PlanningPattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


# Whole-text patterns: matched anywhere in the task description.
PATTERNS: list[PlanningPattern] = [
    PlanningPattern(
        "vague-scope-catchall", "vague-scope", "medium",
        re.compile(r"(?i)\b(as needed|as appropriate|as necessary|and so on|etc\.?)\b"),
        "Open-ended scope marker — state exactly which cases are included.",
    ),
    PlanningPattern(
        "vague-scope-cleanup", "vague-scope", "medium",
        re.compile(r"(?i)\b(clean(?:\s?up)?|improve|handle (?:edge cases|appropriately)|"
                   r"somehow|make .* better)\b"),
        "Unbounded improvement verb — state the concrete, observable change.",
    ),
    PlanningPattern(
        "weak-goal-modal", "weak-goal-modal", "low",
        re.compile(r"(?i)\b(might want to|could probably|maybe|perhaps)\b"),
        "Non-committal goal language — state whether this is actually required.",
    ),
]


# Whole-document absence checks: flagged when the pattern does NOT appear
# anywhere in the task description.
@dataclass(frozen=True)
class AbsencePattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


ABSENCE_PATTERNS: list[AbsencePattern] = [
    AbsencePattern(
        "no-scope-boundary-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(only|just|limited to|excluding|not\s|does not|"
                   r"out of scope|non-goal)\b"),
        "Task description never states a scope boundary — non-goals will "
        "have to be assumed, not derived.",
    ),
    AbsencePattern(
        "no-verification-signal", "unstated-signal", "medium",
        re.compile(r"(?i)\b(test|verify|verification|acceptance|criteria|"
                   r"done when|pass(?:es|ing)?)\b"),
        "Task description never states how completion will be verified — "
        "the test/acceptance hook will have to be assumed, not derived.",
    ),
]
