"""Combines the three ALWAYS-AVAILABLE, non-blended per-file signals —
diff-hygiene flags (Axis 1), structural blast radius (Axis 2), test coverage
(Axis 3) — into one readiness_tier per changed file, via a documented rule
table (ADR-016). Rolls per-file tiers up into one overall_verdict.

Axis 4 (regression_evidence) and Axis 5 (security_evidence) are OPTIONAL,
composed-elsewhere evidence (regression-hunter's overall_risk_tier,
security-context-guard's suggested_verdict) — they stay visible on the
report as distinct fields but do NOT feed this rule table. This is a
deliberate design choice, not an oversight: those two signals are each
already a rolled-up verdict from a DIFFERENT skill's own rule table (ADR-015
for regression risk, ADR-011/the security classification rollup for
security posture) — re-blending an already-rolled-up verdict from one
skill's engine into another skill's rule table would hide which skill
actually produced which judgment, the same "don't collapse the distinction
away" discipline ADR-012/013/014/015 already established for THEIR own
axes. When available, Axis 4/5 evidence is surfaced in warnings for the
agent's Step 3 attention, never silently blended into readiness_tier.

Per-file readiness_tier rule table (checked in order, first match wins):
  1. hygiene_flags non-empty                                  -> blocked
  2. structural_tier == "high" AND NOT has_coverage            -> blocked
  3. structural_tier in ("high", "medium") OR NOT has_coverage -> needs-review
  4. otherwise (structural_tier == "low" AND has_coverage)     -> clear

Overall verdict rollup from per-file tiers:
  any file "blocked"       -> NOT_READY
  any file "needs-review"  -> READY_WITH_CONDITIONS
  otherwise                -> READY

`overall_verdict` is ALWAYS a recommendation for a human to review — see
SKILL.md's Security Constraints and Human Checkpoints sections. This engine
never authorizes a release; it classifies and scores, exactly the same
"advisory only" posture ADR-011 established for security-context-guard.
"""

from __future__ import annotations

from .blast_radius_scorer import structural_tier
from .models import HygieneFlag, StructuralAssessment, TestCoverageStatus


def file_readiness_tier(
    hygiene_flags: list[HygieneFlag],
    structural: StructuralAssessment,
    test_coverage: TestCoverageStatus,
) -> str:
    tier = structural_tier(structural)
    structural.structural_tier = tier
    has_coverage = test_coverage.has_coverage

    if hygiene_flags:
        return "blocked"
    if tier == "high" and not has_coverage:
        return "blocked"
    if tier in ("high", "medium") or not has_coverage:
        return "needs-review"
    return "clear"


def overall_verdict(file_tiers: list[str]) -> str:
    if any(tier == "blocked" for tier in file_tiers):
        return "NOT_READY"
    if any(tier == "needs-review" for tier in file_tiers):
        return "READY_WITH_CONDITIONS"
    return "READY"
