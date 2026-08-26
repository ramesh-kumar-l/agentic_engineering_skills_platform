"""Fixed table of knowledge-capture candidate markers in a free-text
engineering narrative (session notes, a retro, a PR description).

Mirrors architecture-decision's decision_patterns.py / root-cause-
analyzer's symptom_patterns.py shape (project-memory-bank/11-decisions.md
ADR-007, reused an eleventh time here): a fixed keyword/phrase table per
category, non-exhaustive, disclosed as such. Unlike those tables (which
flag *problems* in a document under review), every match here flags a
*candidate for durable capture* — this project's own practice, every phase,
via its L-numbered known-limitations and ADRs (project-memory-bank/
11-decisions.md, 12-known-limitations.md), formalized here as a runnable
tool. A regex match is never itself a verdict that something IS worth
capturing — only the agent's Step 3 Knowledge Capture Checklist walk
(project-memory-bank/05-evaluation-framework.md) makes that call.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgePattern:
    pattern_id: str
    category: str  # "decision" | "lesson" | "limitation" | "workaround"
    regex: re.Pattern[str]
    description: str


PATTERNS: list[KnowledgePattern] = [
    # decision — candidate for an ADR entry
    KnowledgePattern(
        "decision-we-decided", "decision",
        re.compile(r"(?i)\bwe decided\b"),
        "Names a decision this project made — a candidate for an ADR entry "
        "(project-memory-bank/11-decisions.md).",
    ),
    KnowledgePattern(
        "decision-chose-over", "decision",
        re.compile(r"(?i)\bchose\b.{0,60}\bover\b"),
        "Names a choice made between alternatives — a candidate for an ADR entry.",
    ),
    KnowledgePattern(
        "decision-opted-for", "decision",
        re.compile(r"(?i)\bopted for\b"),
        "Names a chosen direction — a candidate for an ADR entry.",
    ),
    KnowledgePattern(
        "decision-tradeoff-was", "decision",
        re.compile(r"(?i)\bthe trade-?off was\b"),
        "States an explicit tradeoff behind a decision — a candidate for an ADR entry.",
    ),
    # lesson — candidate for a lessons-learned entry
    KnowledgePattern(
        "lesson-turns-out", "lesson",
        re.compile(r"(?i)\bturns? out\b"),
        "Surfaces something that wasn't known going in — a candidate for a "
        "lessons-learned entry.",
    ),
    KnowledgePattern(
        "lesson-root-cause-was", "lesson",
        re.compile(r"(?i)\bthe root cause was\b"),
        "Names a confirmed root cause — a candidate for a lessons-learned entry.",
    ),
    KnowledgePattern(
        "lesson-we-learned", "lesson",
        re.compile(r"(?i)\bwe learned\b"),
        "Explicit lesson-learned language — a direct candidate for capture.",
    ),
    KnowledgePattern(
        "lesson-lessons-learned", "lesson",
        re.compile(r"(?i)\blessons? learned\b"),
        "Explicit lesson-learned language — a direct candidate for capture.",
    ),
    # limitation — candidate for a known-limitations entry
    KnowledgePattern(
        "limitation-known-limitation", "limitation",
        re.compile(r"(?i)\bknown limitation\b"),
        "Explicit known-limitation language — a direct candidate for a "
        "known-limitations entry (project-memory-bank/12-known-limitations.md).",
    ),
    KnowledgePattern(
        "limitation-left-unfixed", "limitation",
        re.compile(r"(?i)\bleft unfixed\b"),
        "Names a disclosed-not-fixed gap — a candidate for a known-limitations entry.",
    ),
    KnowledgePattern(
        "limitation-does-not-handle", "limitation",
        re.compile(r"(?i)\bdoes(?:n't| not) handle\b"),
        "Names a scope boundary — a candidate for a known-limitations entry.",
    ),
    KnowledgePattern(
        "limitation-out-of-scope", "limitation",
        re.compile(r"(?i)\bout of scope\b"),
        "Names an explicit scope decision — a candidate for a known-limitations entry.",
    ),
    # workaround — candidate for a known-limitations or lessons-learned entry
    KnowledgePattern(
        "workaround-explicit", "workaround",
        re.compile(r"(?i)\bworkaround\b"),
        "Names a workaround — a candidate for a known-limitations or "
        "lessons-learned entry describing the real fix still owed.",
    ),
    KnowledgePattern(
        "workaround-worked-around-by", "workaround",
        re.compile(r"(?i)\bworked around by\b"),
        "Names how a problem was worked around — a candidate for capture.",
    ),
    KnowledgePattern(
        "workaround-temporary-fix", "workaround",
        re.compile(r"(?i)\btemporary fix\b"),
        "Names a temporary fix — a candidate for capture, and a signal a "
        "real fix is still owed.",
    ),
    KnowledgePattern(
        "workaround-stopgap", "workaround",
        re.compile(r"(?i)\bstop-?gap\b"),
        "Names a stopgap measure — a candidate for capture.",
    ),
]
