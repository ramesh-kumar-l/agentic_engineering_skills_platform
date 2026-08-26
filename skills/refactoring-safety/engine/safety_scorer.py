"""Deterministic risk-tier scoring for each resolved refactor target
(ADR-014).

architecture-decision's ADR-013 scored blast radius from structural data
alone (fan-in/hotspot). This engine adds a second, independent axis: a
structurally risky target that already has a real test module exercising
it is a materially different situation from the same target with none —
the refactor is still risky, but the risk is *covered*, not silent. Rather
than blending "structural risk" and "test coverage" into one number, this
module scores structural risk_tier from operation type + fan_in/hotspot
first, then raises a distinct `untested-blast-radius` flag when that tier
is medium/high and no covering test module was found — so the agent's Step
3 walk always sees both signals separately, never averaged into something
that could look safe for the wrong reason.

Operation-type bands: an operation that changes what a caller sees at the
boundary (rename/delete/move/change-signature/split/merge) is scored
against the target's real fan-in — the more real callers, the more places a
signature change breaks something. An operation that only changes internal
structure without touching the target's public surface (extract/inline) is
scored against hotspot status alone, since callers outside the target
itself are not directly affected by construction.
"""

from __future__ import annotations

from .models import SafetyFlag, TargetAssessment

_BOUNDARY_CHANGING_OPS = {"rename", "delete", "move", "change-signature", "split", "merge"}
_INTERNAL_OPS = {"extract", "inline"}

_HIGH_FAN_IN = 5
_MEDIUM_FAN_IN = 1
_HOTSPOT_MEDIUM_FAN_IN = 2


def _structural_tier(operation_type: str, target: TargetAssessment) -> str:
    if operation_type in _BOUNDARY_CHANGING_OPS:
        if target.is_hotspot or target.fan_in >= _HIGH_FAN_IN:
            return "high"
        if target.fan_in >= _MEDIUM_FAN_IN:
            return "medium"
        return "low"

    if operation_type in _INTERNAL_OPS:
        if target.is_hotspot and target.fan_in >= _HOTSPOT_MEDIUM_FAN_IN:
            return "medium"
        return "low"

    # Generic "refactor" with no more specific operation keyword detected:
    # score conservatively, same band shape as boundary-changing ops, since
    # the actual mechanics are unknown from the text alone.
    if target.is_hotspot or target.fan_in >= _HIGH_FAN_IN:
        return "high"
    if target.fan_in >= _MEDIUM_FAN_IN:
        return "medium"
    return "low"


def score_target(operation_type: str, target: TargetAssessment) -> tuple[str, SafetyFlag | None]:
    tier = _structural_tier(operation_type, target)
    target.risk_tier = tier

    if tier in ("high", "medium") and not target.test_coverage_modules:
        severity = "high" if tier == "high" else "medium"
        flag = SafetyFlag(
            pattern_id="untested-blast-radius",
            category="untested-blast-radius",
            severity=severity,
            description=(
                f"`{target.target_name}` (resolved to "
                f"`{target.resolved_module_path}`) has {tier} structural risk "
                f"(fan_in={target.fan_in}, hotspot={target.is_hotspot}) but no "
                "test module in the codebase-intelligence report imports it — "
                "this refactor's blast radius is real and currently unverified."
            ),
            matched_text=target.target_name,
        )
        return tier, flag

    return tier, None


def score_targets(
    operation_type: str, targets: list[TargetAssessment]
) -> list[SafetyFlag]:
    flags: list[SafetyFlag] = []
    for target in targets:
        if target.resolved_module_path is None:
            continue
        _, flag = score_target(operation_type, target)
        if flag is not None:
            flags.append(flag)
    return flags
