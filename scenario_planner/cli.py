"""Thin CLI entry point. All real logic lives in plan_builder.py.

Usage:
    python -m scenario_planner.cli <test-strategy-report.json> \
        <regression-hunter-report.json> <codebase-intelligence-report.json> \
        [--out DIR]

Requires all three reports for the same target repo — hard preconditions,
not optional context (ADR-010 required-composition pattern, same as
test_strategy's own CLI).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .ci_module_loader import CiModuleLoadError, load_ci_modules
from .plan_builder import build_scenario_plan
from .regression_flags_loader import RegressionFlagsError, load_regression_flags
from .strategy_targets_loader import StrategyReportError, load_strategy_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="scenario-planner", description=__doc__)
    parser.add_argument("strategy_report", help="Path to a test-strategy-report.json")
    parser.add_argument(
        "regression_report",
        help="Path to the regression-hunter report.json for the same repo",
    )
    parser.add_argument(
        "ci_report",
        help="Path to the codebase-intelligence report.json for the same repo",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write scenario-plan-report.json into (default: stdout)",
    )
    args = parser.parse_args(argv)

    try:
        strategy_ctx = load_strategy_report(args.strategy_report)
    except StrategyReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        flags_by_file = load_regression_flags(args.regression_report)
    except RegressionFlagsError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        modules_by_path = load_ci_modules(args.ci_report)
    except CiModuleLoadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = build_scenario_plan(
        strategy_ctx,
        flags_by_file,
        modules_by_path,
        strategy_report_path=str(args.strategy_report),
        regression_report_path=str(args.regression_report),
        ci_report_path=str(args.ci_report),
    )

    output = json.dumps(report.to_dict(), indent=2)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / "scenario-plan-report.json"
        out_path.write_text(output, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
