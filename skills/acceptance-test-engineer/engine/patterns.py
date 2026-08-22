"""Fixed table of mechanically-detectable testability anti-patterns.

These flag *candidates for ambiguity*, not defects — a regex cannot know
whether a requirement is complete, only whether it exhibits a shape known to
correlate with untestable requirements (unquantified adjectives, weak modal
verbs, total silence on error/boundary behavior). The agent's derivation of
actual acceptance test cases (SKILL.md Step 3, against the acceptance-
coverage checklist in project-memory-bank/05-evaluation-framework.md) is what
actually defines correctness; see project-memory-bank/12-known-limitations.md
for this layer's documented false-positive/negative rate.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TestabilityPattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


# Per-sentence patterns: matched against each parsed sentence individually.
PATTERNS: list[TestabilityPattern] = [
    TestabilityPattern(
        "vague-performance-term", "vague-term", "medium",
        re.compile(r"(?i)\b(fast|slow|quick(?:ly)?|responsive|performant)\b"),
        "Unquantified performance term — state a measurable threshold (e.g. 'within 200ms').",
    ),
    TestabilityPattern(
        "vague-quality-term", "vague-term", "medium",
        re.compile(r"(?i)\b(robust|reliable|seamless|intuitive|user[- ]friendly|"
                   r"easy to use|simple|elegant)\b"),
        "Unquantified quality term — state the observable behavior that would prove this.",
    ),
    TestabilityPattern(
        "vague-appropriateness-term", "vague-term", "low",
        re.compile(r"(?i)\b(appropriate(?:ly)?|reasonable|proper(?:ly)?|correctly)\b"),
        "Term defers judgment of correctness to the reader — state the actual rule.",
    ),
    TestabilityPattern(
        "vague-etc-marker", "vague-term", "low",
        re.compile(r"(?i)\b(etc\.?|and so on|and the like|among others)\b"),
        "Open-ended list — enumerate the actual set or state the closure rule.",
    ),
    TestabilityPattern(
        "vague-as-needed", "vague-term", "medium",
        re.compile(r"(?i)\bas (needed|appropriate|necessary)\b"),
        "Defers the actual trigger condition — state exactly when this applies.",
    ),
    TestabilityPattern(
        "weak-modal-should", "weak-modal", "low",
        re.compile(r"(?i)\bshould\b"),
        "'should' is non-binding — state whether this is mandatory ('must') or optional.",
    ),
    TestabilityPattern(
        "weak-modal-could-may", "weak-modal", "low",
        re.compile(r"(?i)\b(could|may)\b"),
        "'could'/'may' signals an unresolved option — state which branch is actually required.",
    ),
]

# Whole-document absence checks: flagged when the pattern does NOT appear
# anywhere in the requirement text.
@dataclass(frozen=True)
class AbsencePattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


ABSENCE_PATTERNS: list[AbsencePattern] = [
    AbsencePattern(
        "no-error-handling-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(invalid|error|exception|fail(?:ure|s)?|reject(?:ed)?|denied|"
                   r"not found|unavailable)\b"),
        "Requirement never mentions error/invalid/failure behavior — acceptance "
        "criteria for the failure path will have to be assumed, not derived.",
    ),
    AbsencePattern(
        "no-boundary-signal", "unstated-signal", "medium",
        re.compile(r"(?i)\b(minimum|maximum|at least|at most|between|limit|threshold|"
                   r"\d+)\b"),
        "Requirement contains no number or explicit bound — boundary/edge-value "
        "acceptance criteria will have to be assumed, not derived.",
    ),
]
