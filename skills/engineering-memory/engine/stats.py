"""Deterministic report-level record/match statistics."""

from __future__ import annotations

from collections import Counter

from .models import MemoryRecord, RelevanceMatch, ReportStats


def compute_stats(records: list[MemoryRecord], matches: list[RelevanceMatch]) -> ReportStats:
    return ReportStats(
        records_scanned=len(records),
        records_scanned_by_type=dict(Counter(r.record_type for r in records)),
        match_count=len(matches),
        match_count_by_status=dict(Counter(m.record.status.value for m in matches)),
    )
