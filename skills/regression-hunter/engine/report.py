"""Orchestrates diff-parse -> ci-report-load -> structural-resolve ->
test-coverage-scan -> diff-pattern-scan -> risk-score -> stats into the
deterministic regression-hunter pre-decision report packet."""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .diff_parser import parse_diff
from .models import FileRiskAssessment, RegressionHunterReport, TestCoverageStatus
from .regression_scanner import scan as scan_regression_patterns
from .risk_scorer import overall_risk_tier
from .stats import compute_stats
from .target_resolver import resolve_file
from .test_coverage_scanner import find_test_coverage


def _file_label(file) -> str:
    return file.effective_path or file.old_path or file.new_path or "<unknown>"


def build_report(diff_text: str, ci_report_path: str) -> RegressionHunterReport:
    ci_report = load_ci_report(ci_report_path)
    diff_context = parse_diff(diff_text)

    assessments: list[FileRiskAssessment] = []
    for file in diff_context.files:
        label = _file_label(file)
        structural = resolve_file(file.effective_path, ci_report)
        coverage_modules = find_test_coverage(structural.resolved_module_path, ci_report)
        test_coverage = TestCoverageStatus(test_coverage_modules=coverage_modules)
        flags = scan_regression_patterns(file, diff_context.files)
        tier = overall_risk_tier(structural, test_coverage, has_flags=bool(flags))

        added = sum(1 for h in file.hunks for l in h.lines if l.kind == "add")
        removed = sum(1 for h in file.hunks for l in h.lines if l.kind == "remove")

        assessments.append(
            FileRiskAssessment(
                file=label,
                is_new_file=file.is_new_file,
                is_deleted_file=file.is_deleted_file,
                lines_added=added,
                lines_removed=removed,
                diff_pattern_flags=flags,
                structural=structural,
                test_coverage=test_coverage,
                overall_risk_tier=tier,
            )
        )

    stats = compute_stats(diff_context.files, assessments)

    warnings: list[str] = list(diff_context.warnings)
    if not diff_text.strip():
        warnings.append("Diff is empty — nothing to assess.")
    if diff_context.files and not any(
        a.structural.resolved_module_path is not None for a in assessments
    ):
        warnings.append(
            "None of the changed files resolved against the codebase-"
            "intelligence report — structural blast radius could not be "
            "derived from real data for this diff."
        )
    if any(a.overall_risk_tier == "high" for a in assessments):
        warnings.append(
            "At least one changed file's overall risk tier is HIGH (a "
            "diff-pattern flag, a high structural tier, or no test "
            "coverage combined with the others per the risk_scorer.py rule "
            "table) — this diff likely warrants closer review before "
            "merging."
        )

    return RegressionHunterReport(stats=stats, files=assessments, warnings=warnings)
