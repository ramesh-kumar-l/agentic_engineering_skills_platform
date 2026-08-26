"""Assigns each scored candidate a CORE/SUPPORTING tier, and — only when
an optional line budget is supplied — an EXCLUDED tier for whatever the
budget cannot fit.

Two independent decisions live here:

1. **Relevance tiering** (budget-independent, `assign_relevance_tiers`):
   `relevance_score >= CORE_THRESHOLD` -> CORE, otherwise SUPPORTING.
   There is no secondary noise-reduction cutoff above zero — any
   candidate that reached this module already scored above zero on real
   keyword relevance (see report.py), and a low-but-nonzero score still
   earns at least SUPPORTING rather than being silently dropped. Many
   systems would apply a stricter minimum to reduce noise; this one
   deliberately does not, because excluding a weakly-relevant file risks
   the worse failure (missing needed context) while including it only
   costs a little budget — see ADR-019.

2. **Budget constraint** (optional, `apply_budget`): walks candidates
   CORE-then-SUPPORTING, both by descending score, accumulating
   line_count. Once the running total would exceed the budget, remaining
   candidates flip to EXCLUDED. The one deliberate exception: a candidate
   whose own line_count alone exceeds the budget is NEVER flipped to
   EXCLUDED — dropping it silently would hide a file the task may
   genuinely need. It keeps its relevance tier, is flagged
   `oversized_alone=True`, and gets a note recommending an excerpt or
   split before loading — a direct callback to this project's own
   <300-line-per-file modularity discipline. This is ADR-019's fail-OPEN-
   under-uncertainty rule: when the budget mechanism itself cannot
   resolve a file cleanly, it flags and keeps rather than silently drops.
"""

from __future__ import annotations

from .models import FileRelevance

CORE_THRESHOLD = 5


def assign_relevance_tiers(candidates: list[FileRelevance]) -> None:
    for c in candidates:
        c.tier = "CORE" if c.relevance_score >= CORE_THRESHOLD else "SUPPORTING"


def apply_budget(candidates: list[FileRelevance], budget_lines: int | None) -> None:
    if budget_lines is None:
        return

    ordered = sorted(candidates, key=lambda c: (c.tier != "CORE", -c.relevance_score))
    running = 0
    for c in ordered:
        if c.line_count > budget_lines:
            c.oversized_alone = True
            c.notes.append(
                "This file's own line count exceeds the budget alone — "
                "recommend excerpting or splitting before loading rather "
                "than dropping it silently."
            )
            running += c.line_count
            continue
        if running + c.line_count > budget_lines:
            c.tier = "EXCLUDED"
            c.notes.append("Excluded — over budget.")
            continue
        running += c.line_count
