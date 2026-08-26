"""Deterministic report-level candidate statistics."""

from __future__ import annotations

from collections import Counter

from .models import KnowledgeCandidate, ReportStats


def compute_stats(candidates: list[KnowledgeCandidate]) -> ReportStats:
    return ReportStats(
        candidate_count=len(candidates),
        candidate_count_by_category=dict(Counter(c.category for c in candidates)),
        candidate_count_by_priority=dict(Counter(c.suggested_capture_priority for c in candidates)),
    )
