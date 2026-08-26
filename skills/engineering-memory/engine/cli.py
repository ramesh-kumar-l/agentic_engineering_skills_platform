"""Thin CLI entry point. All real logic lives in report.py and the renderers.

Usage:
    python -m engine.cli --task "..." --ci-report <report.json> \\
        --decisions-path <11-decisions.md> \\
        --limitations-path <12-known-limitations.md> \\
        [--format json|markdown|both] [--out-dir DIR] [--top-n N]

Reads a free-text task description and a *required* codebase-intelligence
report.json path — hard precondition, reusing project-memory-bank/
11-decisions.md ADR-010's required-composition pattern an ELEVENTH time —
plus this project's own memory-bank markdown files as the self-
referential retrieval corpus (ADR-021).
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
    parser = argparse.ArgumentParser(prog="engineering-memory", description=__doc__)
    parser.add_argument(
        "--task", required=True, help="Free-text task description to retrieve relevant memory for."
    )
    parser.add_argument(
        "--ci-report",
        required=True,
        help="Path to a codebase-intelligence report.json for the target repo "
        "(required — run codebase-intelligence first if it doesn't exist yet).",
    )
    parser.add_argument(
        "--decisions-path",
        required=True,
        help="Path to a project-memory-bank/11-decisions.md-shaped ADR log.",
    )
    parser.add_argument(
        "--limitations-path",
        required=True,
        help="Path to a project-memory-bank/12-known-limitations.md-shaped log.",
    )
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    parser.add_argument(
        "--out-dir", type=Path, default=None, help="Directory to write report files into (default: stdout)"
    )
    parser.add_argument(
        "--top-n", type=int, default=10, help="Maximum number of matches to return (default: 10)."
    )
    args = parser.parse_args(argv)

    for label, path in (
        ("--decisions-path", args.decisions_path),
        ("--limitations-path", args.limitations_path),
    ):
        if not Path(path).exists():
            print(f"error: {label} does not exist: {path}", file=sys.stderr)
            return 1

    try:
        report = build_report(
            task_description=args.task,
            ci_report_path=args.ci_report,
            decisions_path=args.decisions_path,
            limitations_path=args.limitations_path,
            top_n=args.top_n,
        )
    except CiReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["engineering-memory-report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["engineering-memory-report.md"] = render_markdown(report)

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for filename, content in outputs.items():
            (args.out_dir / filename).write_text(content, encoding="utf-8")
            print(f"wrote {args.out_dir / filename}")
    else:
        for content in outputs.values():
            print(content)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
