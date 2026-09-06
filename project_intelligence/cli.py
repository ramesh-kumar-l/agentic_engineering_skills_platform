"""Thin CLI entry point. All real logic lives in profile_builder.py.

Usage:
    python -m project_intelligence.cli <ci-report.json> [--out DIR]

Requires a codebase-intelligence report.json for the target repo — a hard
precondition, not optional context (project-memory-bank/11-decisions.md
ADR-010, same pattern feature-planner already established).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .ci_report_loader import CiReportError
from .profile_builder import build_profile


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="project-intelligence", description=__doc__)
    parser.add_argument(
        "ci_report", help="Path to a codebase-intelligence report.json for the target repo."
    )
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write test-environment-profile.json into (default: stdout)",
    )
    args = parser.parse_args(argv)

    try:
        profile = build_profile(args.ci_report)
    except CiReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output = json.dumps(profile.to_dict(), indent=2)
    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        out_path = args.out / "test-environment-profile.json"
        out_path.write_text(output, encoding="utf-8")
        print(f"wrote {out_path}")
    else:
        print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
