"""Fixed table of mechanically-detectable symptom-quality anti-patterns in a
free-text bug report / failure description.

Mirrors feature-planner's planning anti-pattern table (project-memory-bank/
11-decisions.md ADR-007, reused a fifth time here): these flag *candidates
for an under-specified bug report*, not verdicts — a regex cannot know if
the real root cause will be findable, only whether the symptom description
exhibits wording shapes that correlate with an under-specified report. The
agent's Step 3 investigation (against the Root Cause Investigation checklist
in project-memory-bank/05-evaluation-framework.md) is what actually
diagnoses the failure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SymptomPattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


# Whole-text patterns: matched anywhere in the symptom description.
PATTERNS: list[SymptomPattern] = [
    SymptomPattern(
        "vague-symptom-catchall", "vague-symptom", "medium",
        re.compile(r"(?i)\b(sometimes|randomly|occasionally|out of nowhere|"
                   r"just (?:stopped|broke)|it'?s? broken|doesn'?t work)\b"),
        "Unquantified failure description — state a concrete trigger or "
        "frequency instead of an intermittent/vague characterization.",
    ),
    SymptomPattern(
        "vague-symptom-severity", "vague-symptom", "low",
        re.compile(r"(?i)\b(weird|acts? up|goes? wrong|something(?:'s| is) off|"
                   r"buggy)\b"),
        "Non-specific severity/behavior language — state exactly what output "
        "or behavior was observed.",
    ),
]


# Whole-document absence checks: flagged when the pattern does NOT appear
# anywhere in the symptom description.
@dataclass(frozen=True)
class AbsencePattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


ABSENCE_PATTERNS: list[AbsencePattern] = [
    AbsencePattern(
        "no-expected-actual-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(expected|actual|instead|should (?:have|be)|"
                   r"but (?:got|instead|saw))\b"),
        "Symptom description never states expected vs. actual behavior — "
        "the delta the fix must close will have to be assumed, not derived.",
    ),
    AbsencePattern(
        "no-repro-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(steps? to reproduce|repro|when i|after i|"
                   r"to reproduce|reproduc)\b"),
        "Symptom description never states how to reproduce the failure — "
        "confirmation of any candidate root cause will be harder without it.",
    ),
    AbsencePattern(
        "no-error-signal", "unstated-signal", "medium",
        re.compile(r"(?i)\b(error|exception|traceback|stack trace|"
                   r"fail(?:s|ed|ure)?|crash(?:es|ed)?)\b"),
        "Symptom description never mentions an error message, exception, or "
        "traceback — a stack-trace-grounded candidate location is unlikely.",
    ),
]
