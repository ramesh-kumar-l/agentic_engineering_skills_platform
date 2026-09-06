"""Thin CLI entry point. All real logic lives in generation_planner.py.

Usage:
    python -m test_generation.cli <scenario-plan-report.json> \
        <target-repo-root> [--naming-convention-file PATH] [--out DIR]

Requires a scenario_planner report and the target repo's real root (to
read source excerpts and infer the naming convention) -- hard
preconditions, not optional context (ADR-010 required-composition
pattern, same as scenario_planner's own CLI).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .generation_planner import build_generation_plan
from .naming_convention import (
    NamingConventionError,
    infer_naming_convention,
    load_naming_convention_override,
)
from .scenario_loader import ScenarioPlanError, load_scenario_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="test-generation", description=__doc__)
    parser.add_argument("scenario_plan_report", help="Path to a scenario-plan-report.json")
    parser.add_argument(
        "target_repo_root",
        help="Root of the target repo, to read source excerpts and infer the naming convention",
    )
    parser.add_argument(
        "--naming-convention-file", type=Path, default=None,
        help="Path to a prior run's naming-convention JSON to reuse instead of re-inferring",
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write generation-plan-report.json into (default: stdout)",
    )
    args = parser.parse_args(argv)

    try:
        scenario_ctx = load_scenario_plan(args.scenario_plan_report)
    except ScenarioPlanError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        if args.naming_convention_file:
            naming_convention = load_naming_convention_override(args.naming_convention_file)
        else:
            naming_convention = infer_naming_convention(args.target_repo_root)
    except NamingConventionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    report = build_generation_plan(
        scenario_ctx,
        naming_convention,
        repo_root=str(args.target_repo_root),
        scenario_plan_report_path=str(args.scenario_plan_report),
    )

    output = json.dumps(report.to_dict(), indent=2)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / "generation-plan-report.json"
        out_path.write_text(output, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
