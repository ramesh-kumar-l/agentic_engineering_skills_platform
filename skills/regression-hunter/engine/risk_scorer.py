"""Combines the three explicitly separate regression signals — diff-pattern
flags (Axis 1), structural blast radius (Axis 2), test coverage (Axis 3) —
into one overall_risk_tier per changed file, via a documented rule table
(ADR-015). The three axes remain visible as separate fields on
FileRiskAssessment; this module only computes the roll-up, it never
collapses or discards the underlying axis data.

Structural tiering (Axis 2) reuses refactoring-safety's safety_scorer.py
band shape: a hotspot or fan_in at/above the HIGH threshold is "high"; any
nonzero fan_in below that is "medium"; otherwise "low". Unlike
refactoring-safety, there is no operation-type distinction here — a diff
doesn't parse into one named operation, so every changed file is scored the
same way against its own real fan-in/hotspot data.

Overall-tier rule table (checked in order, first match wins):
  structural=high, (has_flags OR no_coverage)        -> HIGH
  structural=high, has_coverage AND not has_flags     -> MEDIUM
  structural=medium, has_flags AND no_coverage        -> HIGH
  structural=medium, (has_flags OR no_coverage)       -> MEDIUM
  structural=medium, has_coverage AND not has_flags   -> LOW
  structural=low, has_flags AND no_coverage           -> MEDIUM
  structural=low, otherwise                           -> LOW

Rationale: a structurally high-blast-radius file is never downgraded below
MEDIUM even when it's covered and flag-free, because real callers exist and
a diff-pattern scan cannot prove behavioral equivalence — only a genuinely
covered, flag-free, high-blast-radius file avoids the top tier. A flagged
change with zero test coverage escalates one tier at every structural
level, since an unflagged-but-untested change and a flagged-and-tested
change are each a different, real kind of risk, not interchangeable.
"""

from __future__ import annotations

from .models import StructuralAssessment, TestCoverageStatus

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


def overall_risk_tier(
    structural: StructuralAssessment,
    test_coverage: TestCoverageStatus,
    has_flags: bool,
) -> str:
    tier = structural_tier(structural)
    structural.structural_tier = tier
    has_coverage = test_coverage.has_coverage

    if tier == "high":
        return "high" if (has_flags or not has_coverage) else "medium"

    if tier == "medium":
        if has_flags and not has_coverage:
            return "high"
        if has_flags or not has_coverage:
            return "medium"
        return "low"

    # tier == "low"
    if has_flags and not has_coverage:
        return "medium"
    return "low"
