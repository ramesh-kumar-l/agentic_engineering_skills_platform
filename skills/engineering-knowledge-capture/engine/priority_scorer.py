"""Deterministic suggested_capture_priority rollup: combines a candidate's
resolved structural location (if any) with real fan_in/hotspot data from
the composed codebase-intelligence report.

Reuses the fail-closed-under-uncertainty discipline security-context-
guard's ADR-011 and dependency-supply-chain's ADR-017 established: an
UNRESOLVED candidate (no module mentioned, or a mentioned module the CI
report doesn't recognize) or a candidate scored against a CI report that
itself carried a warning (e.g. zero modules parsed) never scores LOW — it
fails closed to MEDIUM, never silently deprioritized.

LOW is a defined band (see models.py) that this version's scorer never
actually assigns: a resolved-but-structurally-unremarkable candidate (a
real module, zero fan-in, not a hotspot) would be the natural case for it,
but this version deliberately defaults such cases to MEDIUM as well —
failing UPWARD, not downward, matches this skill's whole purpose (missing
a real candidate for capture is worse than reviewing one extra that turns
out not to matter). Named explicitly in SKILL.md Known Limitations, not
left as a silent gap in the enum.
"""

from __future__ import annotations

from .models import ResolvedLocation

# Simple, disclosed fixed threshold — not derived from the composed
# report's own fan_in distribution, unlike some other skills' percentile-
# based tiers (e.g. architecture-decision's impact_scorer.py). See SKILL.md
# Known Limitations.
HIGH_FAN_IN_THRESHOLD = 3


def compute_priority(resolved: ResolvedLocation | None, ci_has_warning: bool) -> str:
    if ci_has_warning or resolved is None:
        return "MEDIUM"
    if resolved.is_hotspot or resolved.fan_in >= HIGH_FAN_IN_THRESHOLD:
        return "HIGH"
    return "MEDIUM"
