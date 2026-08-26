"""Deterministic report-level flag statistics — separate from surface_area.py
(which describes the dependency population itself) so each stays under the
project's single-responsibility-per-module convention.
"""

from __future__ import annotations

from collections import Counter

from .models import ReportStats, RiskFlag


def compute_stats(flags: list[RiskFlag]) -> ReportStats:
    return ReportStats(
        flag_count=len(flags),
        flag_count_by_severity=dict(Counter(f.severity for f in flags)),
        flag_count_by_category=dict(Counter(f.category for f in flags)),
    )
