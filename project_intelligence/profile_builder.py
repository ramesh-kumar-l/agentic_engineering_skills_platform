"""Assembles a TestEnvironmentProfile from a codebase-intelligence report.

The only integration point with codebase-intelligence is its already-
produced report.json — no import of its `engine` package, matching the
same decoupling ADR-010/ADR-024 already established for this portfolio.
"""

from __future__ import annotations

from pathlib import Path

from .ci_report_loader import CiReportContext, load_ci_report
from .detect import (
    detect_android_test_frameworks,
    detect_build_systems,
    detect_coverage_tools,
    detect_mock_frameworks,
    detect_test_frameworks,
)
from .models import SCHEMA_VERSION, TestEnvironmentProfile
from .signatures import ANDROID_TARGET_FRAMEWORKS

_CATEGORY_LABELS = {
    "build_systems": "build_system",
    "test_frameworks": "test_framework",
    "mock_frameworks": "mock_framework",
    "coverage_tools": "coverage_tool",
    "android_test_frameworks": "android_test_framework",
}


def _primary_language(language_breakdown: dict[str, int]) -> str | None:
    if not language_breakdown:
        return None
    return max(language_breakdown, key=lambda lang: language_breakdown[lang])


def build_profile(ci_report_path: str | Path) -> TestEnvironmentProfile:
    ctx: CiReportContext = load_ci_report(ci_report_path)

    findings = {
        "build_systems": detect_build_systems(ctx),
        "test_frameworks": detect_test_frameworks(ctx),
        "mock_frameworks": detect_mock_frameworks(ctx),
        "coverage_tools": detect_coverage_tools(ctx),
        "android_test_frameworks": detect_android_test_frameworks(ctx),
    }

    unavailable = [
        _CATEGORY_LABELS[category] for category, results in findings.items() if not results
    ]

    android_frameworks_absent = sorted(
        set(ANDROID_TARGET_FRAMEWORKS)
        - {f.name for f in findings["android_test_frameworks"]}
    )

    warnings = []
    if not ctx.external_dependencies:
        warnings.append(
            "codebase-intelligence reported zero external_dependencies for this "
            "scan root — dependency-confirmed detection is impossible here; any "
            "build-system findings below are manifest-only (see project-memory-"
            "bank/12-known-limitations.md L2/L34 for why this can under-report)."
        )

    return TestEnvironmentProfile(
        schema_version=SCHEMA_VERSION,
        repo_root=ctx.root_path,
        ci_report_path=str(ci_report_path),
        primary_language=_primary_language(ctx.language_breakdown),
        language_breakdown=ctx.language_breakdown,
        build_systems=findings["build_systems"],
        test_frameworks=findings["test_frameworks"],
        mock_frameworks=findings["mock_frameworks"],
        coverage_tools=findings["coverage_tools"],
        android_test_frameworks=findings["android_test_frameworks"],
        android_frameworks_absent=android_frameworks_absent,
        unavailable=unavailable,
        warnings=warnings,
    )
