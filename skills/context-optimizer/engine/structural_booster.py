"""Boosts a file's keyword-relevance score using real fan_in/hotspot data
from the composed codebase-intelligence report — the same "a structural
signal is a real, additive input, never the sole basis for a judgment"
convention architecture-decision's `impact_scorer.py` and
refactoring-safety's/regression-hunter's risk scoring already established
(ADR-013 lineage). A file only reaches this booster after already scoring
above zero on keyword relevance (see report.py) — structural significance
alone never manufactures relevance out of nothing.
"""

from __future__ import annotations

from .models import CiDependencyGraph

HIGH_FAN_IN_THRESHOLD = 3
HOTSPOT_BOOST = 3
HIGH_FAN_IN_BOOST = 1


def apply_structural_boost(base_score: int, path: str, graph: CiDependencyGraph) -> int:
    if path in graph.hotspots:
        return base_score + HOTSPOT_BOOST
    if graph.fan_in.get(path, 0) >= HIGH_FAN_IN_THRESHOLD:
        return base_score + HIGH_FAN_IN_BOOST
    return base_score
