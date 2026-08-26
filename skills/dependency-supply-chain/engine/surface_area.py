"""Deterministic surface-area statistics: how many direct dependencies exist
and what fraction are unpinned, as a simple proxy for supply-chain attack
surface (more direct dependencies, and more of them unpinned, means more
opportunity for an unreviewed/compromised version to land silently).
"""

from __future__ import annotations

from collections import Counter

from .models import DependencyRecord, SurfaceAreaStats
from .pin_checker import is_unpinned


def compute_surface_area(records: list[DependencyRecord]) -> SurfaceAreaStats:
    total = len(records)
    unpinned = sum(1 for r in records if is_unpinned(r.pin_status))
    breakdown = Counter(r.source_file for r in records)

    return SurfaceAreaStats(
        total_dependencies=total,
        unpinned_count=unpinned,
        unpinned_percentage=round((unpinned / total * 100), 1) if total else 0.0,
        manifest_breakdown=dict(breakdown),
    )
