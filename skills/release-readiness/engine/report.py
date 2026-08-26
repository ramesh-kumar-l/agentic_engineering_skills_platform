"""Orchestrates diff-parse -> ci-report-load -> structural-resolve ->
test-coverage-scan -> hygiene-scan -> [optional regression/security evidence
load] -> readiness-score -> stats into the deterministic release-readiness
pre-decision report packet."""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .diff_parser import parse_diff
from .hygiene_scanner import scan as scan_hygiene
from .models import (
    FileReadinessAssessment,
    ReleaseReadinessReport,
    RegressionEvidence,
    TestCoverageStatus,
)
from .readiness_scorer import file_readiness_tier, overall_verdict
from .regression_report_loader import load_regression_evidence
from .security_report_loader import load_security_evidence
from .stats import compute_stats
from .target_resolver import resolve_file
from .test_coverage_scanner import find_test_coverage


def _file_label(file) -> str:
    return file.effective_path or file.old_path or file.new_path or "<unknown>"


def build_report(
    diff_text: str,
    ci_report_path: str,
    regression_report_path: str | None = None,
    security_report_path: str | None = None,
) -> ReleaseReadinessReport:
    ci_report = load_ci_report(ci_report_path)
    diff_context = parse_diff(diff_text)
    regression_evidence_by_file, regression_warnings = load_regression_evidence(
        regression_report_path
    )
    security_evidence, security_warnings = load_security_evidence(security_report_path)

    assessments: list[FileReadinessAssessment] = []
    for file in diff_context.files:
        label = _file_label(file)
        structural = resolve_file(file.effective_path, ci_report)
        coverage_modules = find_test_coverage(structural.resolved_module_path, ci_report)
        test_coverage = TestCoverageStatus(test_coverage_modules=coverage_modules)
        hygiene_flags = scan_hygiene(file)
        regression_evidence = regression_evidence_by_file.get(label, RegressionEvidence())
        tier = file_readiness_tier(hygiene_flags, structural, test_coverage)

        added = sum(1 for h in file.hunks for l in h.lines if l.kind == "add")
        removed = sum(1 for h in file.hunks for l in h.lines if l.kind == "remove")

        assessments.append(
            FileReadinessAssessment(
                file=label,
                is_new_file=file.is_new_file,
                is_deleted_file=file.is_deleted_file,
                lines_added=added,
                lines_removed=removed,
                hygiene_flags=hygiene_flags,
                structural=structural,
                test_coverage=test_coverage,
                regression_evidence=regression_evidence,
                readiness_tier=tier,
            )
        )

    stats = compute_stats(diff_context.files, assessments)
    verdict = overall_verdict([a.readiness_tier for a in assessments])

    warnings: list[str] = list(diff_context.warnings)
    warnings.extend(regression_warnings)
    warnings.extend(security_warnings)
    if not diff_text.strip():
        warnings.append(
            "Diff is empty — nothing to assess; overall_verdict is not "
            "meaningful for an empty diff."
        )
    if diff_context.files and not any(
        a.structural.resolved_module_path is not None for a in assessments
    ):
        warnings.append(
            "None of the changed files resolved against the codebase-"
            "intelligence report — structural blast radius could not be "
            "derived from real data for this diff."
        )
    if any(a.readiness_tier == "blocked" for a in assessments):
        warnings.append(
            "At least one changed file's readiness tier is BLOCKED (a "
            "diff-hygiene flag, or high structural blast radius with no "
            "test coverage) — this diff is NOT recommended for release "
            "without further changes."
        )
    if security_evidence.available and security_evidence.suggested_verdict == "REQUIRES_HUMAN_APPROVAL":
        warnings.append(
            "The composed security-context-guard report's suggested_verdict "
            "is REQUIRES_HUMAN_APPROVAL — surfaced as-is, not re-derived; "
            "this does not automatically change overall_verdict (see "
            "readiness_scorer.py), but a human should weigh it explicitly."
        )

    return ReleaseReadinessReport(
        stats=stats,
        files=assessments,
        overall_verdict=verdict,
        regression_report_composed=bool(regression_evidence_by_file),
        security_report_composed=security_evidence.available,
        security_evidence=security_evidence,
        warnings=warnings,
    )
