"""Orchestrates ci-report-load -> operation-parse -> target-resolve ->
test-coverage-scan -> safety-score -> text-scan -> stats into the
deterministic refactoring-safety pre-decision report packet."""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .models import RefactoringSafetyReport
from .operation_parser import parse_operation
from .safety_scanner import scan
from .safety_scorer import score_targets
from .stats import compute_stats
from .target_resolver import resolve_targets
from .test_coverage_scanner import find_test_coverage


def build_report(refactor_text: str, ci_report_path: str) -> RefactoringSafetyReport:
    ci_report = load_ci_report(ci_report_path)
    operation_type, raw_targets = parse_operation(refactor_text)
    targets = resolve_targets(raw_targets, ci_report)

    for target in targets:
        target.test_coverage_modules = find_test_coverage(
            target.resolved_module_path, ci_report
        )

    derived_flags = score_targets(operation_type, targets)
    text_flags = scan(refactor_text)
    flags = text_flags + derived_flags
    stats = compute_stats(refactor_text, targets, flags)

    warnings: list[str] = []
    if not refactor_text.strip():
        warnings.append("Refactor description is empty.")
    if not targets:
        warnings.append(
            "No target identifiers were parsed from the refactor description "
            "— name the specific module/function/class being refactored "
            "(quoted or backticked identifiers are matched with the highest "
            "confidence, e.g. `foo.py` or `bar_function`)."
        )
    elif not any(t.resolved_module_path is not None for t in targets):
        warnings.append(
            "None of the parsed targets matched any module, function, or "
            "class in the codebase-intelligence report — blast radius could "
            "not be derived from real structural data for this refactor."
        )
    if any(t.risk_tier == "high" for t in targets):
        warnings.append(
            "At least one target's risk tier is HIGH (touches a hotspot or "
            "high fan-in module with a boundary-changing operation) — this "
            "refactor likely warrants wider review before proceeding."
        )
    if any(f.category == "untested-blast-radius" for f in flags):
        warnings.append(
            "At least one structurally risky target has no matching test "
            "module in the codebase-intelligence report — treat this as "
            "unverified, not safe, until real test coverage is confirmed."
        )

    return RefactoringSafetyReport(
        refactor_text=refactor_text,
        operation_type=operation_type,
        stats=stats,
        flags=flags,
        targets=targets,
        warnings=warnings,
    )
