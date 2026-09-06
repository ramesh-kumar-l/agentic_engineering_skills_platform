"""Composes a ValidationReport by running validation_runner over every
agent-authored test file found in a directory (TEP Phase 5c).
"""

from __future__ import annotations

from .environment_loader import TestEnvironmentSummary
from .generated_tests_loader import list_generated_tests
from .models import SCHEMA_VERSION, ValidationReport, ValidationStats
from .validation_runner import DEFAULT_TIMEOUT_SECONDS, run_validation


def build_validation_report(
    generated_tests_dir: str,
    profile: TestEnvironmentSummary,
    repo_root: str,
    test_environment_profile_path: str,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
) -> ValidationReport:
    test_files = list_generated_tests(generated_tests_dir)

    outcomes = [
        run_validation(f, repo_root, profile.primary_test_framework, timeout_seconds)
        for f in test_files
    ]

    warnings: list[str] = []
    if not test_files:
        warnings.append(
            "no agent-authored test files found under "
            f"{generated_tests_dir} — nothing to validate"
        )

    stats = ValidationStats(
        test_files_considered=len(outcomes),
        passed=sum(1 for o in outcomes if o.passed),
        failed=sum(1 for o in outcomes if not o.passed and not o.timed_out),
        timed_out=sum(1 for o in outcomes if o.timed_out),
    )

    return ValidationReport(
        schema_version=SCHEMA_VERSION,
        repo_root=repo_root,
        generated_tests_dir=str(generated_tests_dir),
        test_environment_profile_path=test_environment_profile_path,
        stats=stats,
        outcomes=outcomes,
        warnings=warnings,
    )
