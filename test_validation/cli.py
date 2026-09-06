"""Thin CLI entry point. All real logic lives in report_builder.py.

Usage:
    python -m test_validation.cli <generated-tests-dir> \
        <test-environment-profile.json> <target-repo-root> \
        [--timeout SECONDS] [--out DIR]

Executes every agent-authored test file found under <generated-tests-dir>
against the target repo via subprocess -- this platform's first execution
capability. No sandboxing beyond a process-level timeout is claimed; see
validation_runner.py's own disclosure.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .environment_loader import ProfileLoadError, load_test_environment_profile
from .generated_tests_loader import GeneratedTestsError
from .report_builder import (
    DEFAULT_MAX_TEST_FILE_BYTES,
    DEFAULT_MAX_TEST_FILES,
    build_validation_report,
)
from .validation_runner import DEFAULT_TIMEOUT_SECONDS, PytestUnavailableError


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="test-validation", description=__doc__)
    parser.add_argument("generated_tests_dir", help="Directory of agent-authored test files")
    parser.add_argument(
        "profile",
        help="Path to a project_intelligence test-environment-profile.json for the target repo",
    )
    parser.add_argument(
        "target_repo_root", help="Root of the target repo, importable at execution time"
    )
    parser.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS,
        help=f"Per-file subprocess timeout in seconds (default: {DEFAULT_TIMEOUT_SECONDS})",
    )
    parser.add_argument(
        "--max-test-files", type=int, default=DEFAULT_MAX_TEST_FILES,
        help=f"Max test files executed per run (default: {DEFAULT_MAX_TEST_FILES})",
    )
    parser.add_argument(
        "--max-test-file-bytes", type=int, default=DEFAULT_MAX_TEST_FILE_BYTES,
        help=f"Max size in bytes of a single test file executed (default: {DEFAULT_MAX_TEST_FILE_BYTES})",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write validation-report.json into (default: stdout)",
    )
    args = parser.parse_args(argv)

    try:
        profile = load_test_environment_profile(args.profile)
    except ProfileLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        report = build_validation_report(
            args.generated_tests_dir,
            profile,
            repo_root=str(args.target_repo_root),
            test_environment_profile_path=str(args.profile),
            timeout_seconds=args.timeout,
            max_test_files=args.max_test_files,
            max_test_file_bytes=args.max_test_file_bytes,
        )
    except (GeneratedTestsError, PytestUnavailableError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(report.to_dict(), indent=2)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / "validation-report.json"
        out_path.write_text(output, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
