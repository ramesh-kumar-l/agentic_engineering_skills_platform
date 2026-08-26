"""Applies knowledge_patterns.py's marker table to a free-text engineering
narrative, returning one KnowledgeCandidate per match — not just the first
match per pattern. A narrative can genuinely describe several decisions,
lessons, limitations, or workarounds in one document; collapsing repeats
into one flag would hide real candidates from the agent's Step 3 walk, the
same "don't collapse away findings" discipline dependency-supply-chain's
scanner.py already established for its own compounding-case fixture.
"""

from __future__ import annotations

from .knowledge_patterns import PATTERNS
from .models import KnowledgeCandidate


def _line_for_offset(text: str, offset: int, lines: list[str]) -> str:
    line_no = text.count("\n", 0, offset)
    return lines[line_no] if line_no < len(lines) else ""


def scan(narrative_text: str) -> list[KnowledgeCandidate]:
    candidates: list[KnowledgeCandidate] = []
    lines = narrative_text.splitlines()

    for pattern in PATTERNS:
        for match in pattern.regex.finditer(narrative_text):
            evidence_line = _line_for_offset(narrative_text, match.start(), lines).strip()
            candidates.append(
                KnowledgeCandidate(
                    pattern_id=pattern.pattern_id,
                    category=pattern.category,
                    matched_text=match.group(0),
                    description=pattern.description,
                    evidence=evidence_line or match.group(0),
                )
            )

    return candidates
