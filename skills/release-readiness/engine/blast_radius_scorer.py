"""Computes Axis 2 — structural blast-radius tier — from a resolved file's
real fan-in/hotspot data. Reuses architecture-decision's/refactoring-
safety's/regression-hunter's tiering band shape (ADR-013/014/015 lineage):
a hotspot or fan_in at/above the HIGH threshold is "high"; any nonzero
fan_in below that is "medium"; otherwise "low". An unresolved file (no
structural data available) is "low" — not because it's known to be safe,
but because the engine has nothing to ground a higher tier on; the agent's
Step 3 walk must not read "low" as "verified safe" for an unresolved file
(same caution as every prior skill's structural scorer, and stated
explicitly in SKILL.md's Agent Responsibilities).
"""

from __future__ import annotations

from .models import StructuralAssessment

_HIGH_FAN_IN = 5
_MEDIUM_FAN_IN = 1


def structural_tier(assessment: StructuralAssessment) -> str:
    if assessment.resolved_module_path is None:
        return "low"
    if assessment.is_hotspot or assessment.fan_in >= _HIGH_FAN_IN:
        return "high"
    if assessment.fan_in >= _MEDIUM_FAN_IN:
        return "medium"
    return "low"
