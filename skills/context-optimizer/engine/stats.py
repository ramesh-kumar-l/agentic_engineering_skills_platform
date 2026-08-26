"""Deterministic report-level recommendation statistics."""

from __future__ import annotations

from collections import Counter

from .models import FileRelevance, ReportStats


def compute_stats(candidates: list[FileRelevance]) -> ReportStats:
    return ReportStats(
        candidate_count=len(candidates),
        candidate_count_by_tier=dict(Counter(c.tier for c in candidates)),
        total_estimated_tokens=sum(
            c.estimated_tokens for c in candidates if c.tier != "EXCLUDED"
        ),
        oversized_alone_count=sum(1 for c in candidates if c.oversized_alone),
    )
