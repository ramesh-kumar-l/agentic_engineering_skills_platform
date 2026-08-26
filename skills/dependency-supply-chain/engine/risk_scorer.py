"""Deterministic rollup: turns the flag list into a `suggested_risk_level`.
Reuses security-context-guard's ADR-011 discipline — this value is ALWAYS
advisory, never a merge/release gate the engine enforces itself; only a
human (via the agent's workflow) makes the real decision. Fails closed to
"REQUIRES_REVIEW" on any high-severity flag or on ambiguous evidence (zero
dependencies parsed, or the CI report carried warnings) rather than
defaulting to "CLEAR" when the picture is unclear.
"""

from __future__ import annotations

from .models import RiskFlag


def compute_risk_level(flags: list[RiskFlag], dependency_count: int, ci_warnings: list[str]) -> str:
    if dependency_count == 0 or ci_warnings:
        return "REQUIRES_REVIEW"

    if any(f.severity == "high" for f in flags):
        return "REQUIRES_REVIEW"

    if any(f.severity == "medium" for f in flags):
        return "NEEDS_REVIEW"

    if any(f.severity == "low" for f in flags):
        return "NEEDS_REVIEW"

    return "CLEAR"
