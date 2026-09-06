"""Combines regression-hunter's per-file risk signals with a
project_intelligence TestEnvironmentProfile to decide which changed files
need a regression test (TEP Phase 5a).

Priority is copied directly from regression-hunter's own overall_risk_tier
vocabulary ("high"/"medium"/"low") — this module never computes a
competing score, only filters (already-covered files are dropped) and
attaches an environment-feasibility verdict.
"""

from __future__ import annotations

from .models import SCHEMA_VERSION, TestStrategyReport, TestStrategyStats, TestTarget
from .profile_loader import TestEnvironmentSummary
from .regression_report_loader import RegressionReportContext

_PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}

_REASON_BY_TIER = {
    "high": (
        "regression-hunter scored this file's overall_risk_tier as high "
        "and found no covering test module"
    ),
    "medium": (
        "regression-hunter scored this file's overall_risk_tier as medium "
        "and found no covering test module"
    ),
    "low": (
        "no covering test module was found for this changed file "
        "(informational — regression-hunter's overall_risk_tier is low)"
    ),
}


def build_strategy(
    regression_ctx: RegressionReportContext,
    profile: TestEnvironmentSummary,
    regression_report_path: str,
    profile_path: str,
) -> TestStrategyReport:
    if profile.primary_test_framework is not None:
        feasible = True
        feasibility_note = (
            f"a test framework ({profile.primary_test_framework}) was "
            "detected for this repo"
        )
    else:
        feasible = False
        feasibility_note = (
            "no test framework was detected for this repo (see "
            "TestEnvironmentProfile.unavailable) — generation would "
            "require a human decision on which framework/convention to "
            "use, never a guess"
        )

    targets: list[TestTarget] = []
    already_covered = 0

    for f in regression_ctx.files:
        if f.is_deleted_file:
            continue
        if f.has_test_coverage:
            already_covered += 1
            continue
        tier = f.overall_risk_tier
        targets.append(
            TestTarget(
                file=f.file,
                priority=tier if tier in _PRIORITY_RANK else "low",
                reason=_REASON_BY_TIER.get(tier, _REASON_BY_TIER["low"]),
                risk_tier=tier,
                generation_feasible=feasible,
                feasibility_note=feasibility_note,
                recommended_framework=profile.primary_test_framework,
            )
        )

    targets.sort(key=lambda t: _PRIORITY_RANK.get(t.priority, 3))

    warnings: list[str] = []
    if not regression_ctx.files:
        warnings.append(
            "regression-hunter report contained zero changed files — "
            "nothing to strategize about"
        )

    stats = TestStrategyStats(
        files_considered=len(regression_ctx.files),
        files_already_covered=already_covered,
        targets_flagged=len(targets),
        high_priority_count=sum(1 for t in targets if t.priority == "high"),
        medium_priority_count=sum(1 for t in targets if t.priority == "medium"),
        low_priority_count=sum(1 for t in targets if t.priority == "low"),
    )

    return TestStrategyReport(
        schema_version=SCHEMA_VERSION,
        repo_root=profile.repo_root,
        regression_report_path=regression_report_path,
        profile_path=profile_path,
        stats=stats,
        targets=targets,
        warnings=warnings,
    )
