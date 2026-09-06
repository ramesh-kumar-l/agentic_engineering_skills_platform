"""Thin CLI entry point. All real logic lives in strategy_builder.py.

Usage:
    python -m test_strategy.cli <regression-hunter-report.json> \
        <test-environment-profile.json> [--out DIR]

Requires both a regression-hunter report.json and a project_intelligence
test-environment-profile.json for the same target repo — hard
preconditions, not optional context (ADR-010 required-composition
pattern, same as project_intelligence's own CLI).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .profile_loader import ProfileLoadError, load_test_environment_profile
from .regression_report_loader import RegressionReportError, load_regression_report
from .strategy_builder import build_strategy


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="test-strategy", description=__doc__)
    parser.add_argument("regression_report", help="Path to a regression-hunter report.json")
    parser.add_argument(
        "profile",
        help="Path to a project_intelligence test-environment-profile.json for the same repo",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write test-strategy-report.json into (default: stdout)",
    )
    args = parser.parse_args(argv)

    try:
        regression_ctx = load_regression_report(args.regression_report)
    except RegressionReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        profile = load_test_environment_profile(args.profile)
    except ProfileLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = build_strategy(
        regression_ctx,
        profile,
        regression_report_path=str(args.regression_report),
        profile_path=str(args.profile),
    )

    output = json.dumps(report.to_dict(), indent=2)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / "test-strategy-report.json"
        out_path.write_text(output, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
