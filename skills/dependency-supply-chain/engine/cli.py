"""Thin CLI entry point. All real logic lives in report.py and the renderers.

Usage:
    python -m engine.cli --ci-report <report.json> [--format json|markdown|both] [--out DIR]

A codebase-intelligence report.json is a *required* precondition, not
optional context — reusing project-memory-bank/11-decisions.md ADR-010's
required-composition pattern a seventh time.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ci_report_loader import CiReportError
from .render_json import render_json
from .render_markdown import render_markdown
from .report import build_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dependency-supply-chain", description=__doc__)
    parser.add_argument(
        "--ci-report", required=True,
        help="Path to a codebase-intelligence report.json for the target repo "
             "(required — run codebase-intelligence first if it doesn't exist yet).",
    )
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write report files into (default: stdout)",
    )
    args = parser.parse_args(argv)

    try:
        report = build_report(args.ci_report)
    except CiReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["dependency-supply-chain-report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["dependency-supply-chain-report.md"] = render_markdown(report)

    if args.out:
        args.out.mkdir(parents=True, exist_ok=True)
        for filename, content in outputs.items():
            (args.out / filename).write_text(content, encoding="utf-8")
            print(f"wrote {args.out / filename}")
    else:
        for content in outputs.values():
            print(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
