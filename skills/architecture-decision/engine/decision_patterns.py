"""Fixed table of mechanically-detectable decision-quality anti-patterns in a
free-text architecture-decision description.

Mirrors root-cause-analyzer's symptom anti-pattern table (project-memory-bank/
11-decisions.md ADR-007, reused a sixth time here): these flag *candidates
for an under-specified decision*, not verdicts — a regex cannot know if a
decision is actually reversible or actually weighed real tradeoffs, only
whether the decision text exhibits wording shapes that correlate with a
decision made without them. The agent's Step 3 walk against the Architecture
Decision Record checklist (project-memory-bank/05-evaluation-framework.md)
is what actually judges decision quality.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionPattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


# Whole-text patterns: matched anywhere in the decision description.
PATTERNS: list[DecisionPattern] = [
    DecisionPattern(
        "vague-decision-language", "vague-decision", "medium",
        re.compile(r"(?i)\b(just|simply|obviously|clearly|trivial(?:ly)?|"
                   r"easy|should be fine|no big deal)\b"),
        "Confidence language with no supporting evidence — state the actual "
        "reasoning or data behind the claim instead of asserting it's easy/obvious.",
    ),
]


# Whole-document absence checks: flagged when the pattern does NOT appear
# anywhere in the decision description.
@dataclass(frozen=True)
class AbsencePattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


ABSENCE_PATTERNS: list[AbsencePattern] = [
    AbsencePattern(
        "no-alternatives-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(option|alternative|instead of|vs\.?|versus|"
                   r"rather than)\b"),
        "Decision text never names an alternative that was considered — a "
        "decision with exactly one path on the table is a proposal, not a "
        "comparison; the checklist's alternatives category will have to be "
        "stated as an assumption rather than derived.",
    ),
    AbsencePattern(
        "no-reversibility-signal", "unstated-signal", "high",
        re.compile(r"(?i)\b(revert|rollback|reversible|irreversible|"
                   r"undo|migrate back|one-way door|two-way door)\b"),
        "Decision text never addresses whether this choice is reversible — "
        "reversibility materially changes how much upfront certainty a "
        "decision needs before proceeding.",
    ),
    AbsencePattern(
        "no-tradeoff-signal", "unstated-signal", "medium",
        re.compile(r"(?i)\b(tradeoff|trade-off|trades?\b|downside|drawback|"
                   r"cost|risk|con(?:s)?\b|however|but\b|at the expense of)\b"),
        "Decision text never states a downside or cost of the chosen "
        "direction — a decision with no stated tradeoffs reads as a "
        "one-sided pitch rather than a weighed comparison.",
    ),
    AbsencePattern(
        "no-security-signal", "unstated-signal", "low",
        re.compile(r"(?i)\b(security|secret|auth(?:entication|orization)?|"
                   r"permission|access control|credential|encrypt)\b"),
        "Decision text never mentions security implications — this may be "
        "genuinely N/A for this decision; state that explicitly rather than "
        "silently omitting the category.",
    ),
]
