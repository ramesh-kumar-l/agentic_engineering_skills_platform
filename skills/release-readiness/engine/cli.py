"""Thin CLI entry point. All real logic lives in report.py and the renderers.

Usage:
    python -m engine.cli <diff-file-or-'-'> --ci-report <report.json> \
        [--regression-report <report.json>] [--security-report <report.json>] \
        [--format json|markdown|both] [--out DIR]

Reads unified diff text (git-style or plain) from a file path or stdin, and
a *required* codebase-intelligence report.json path — this is a hard
precondition, not optional context, reusing project-memory-bank/
11-decisions.md ADR-010's required-composition pattern a sixth time.
--regression-report and --security-report are both OPTIONAL — omitting
either is simply absent evidence, not a failure (ADR-011 precedent).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .ci_report_loader import CiReportError
from .render_json import render_json
from .render_markdown import render_markdown
from .report import build_report


def _read_diff_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="release-readiness", description=__doc__)
    parser.add_argument(
        "path", help="Path to a unified-diff text file, or '-' to read from stdin."
    )
    parser.add_argument(
        "--ci-report", required=True,
        help="Path to a codebase-intelligence report.json for the target repo "
             "(required — run codebase-intelligence first if it doesn't exist yet).",
    )
    parser.add_argument(
        "--regression-report", default=None,
        help="Optional path to a regression-hunter report.json for this same "
             "diff — surfaced as Axis 4 evidence, not re-derived. Omitting "
             "this is not a failure.",
    )
    parser.add_argument(
        "--security-report", default=None,
        help="Optional path to a security-context-guard report.json — "
             "surfaced as Axis 5 evidence, not re-derived. Omitting this is "
             "not a failure.",
    )
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    parser.add_argument(
        "--out", type=Path, default=None,
        help="Directory to write report files into (default: stdout)",
    )
    args = parser.parse_args(argv)

    if args.path != "-" and not Path(args.path).exists():
        print(f"error: path does not exist: {args.path}", file=sys.stderr)
        return 1

    diff_text = _read_diff_text(args.path)

    try:
        report = build_report(
            diff_text,
            args.ci_report,
            regression_report_path=args.regression_report,
            security_report_path=args.security_report,
        )
    except CiReportError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["release-readiness-report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["release-readiness-report.md"] = render_markdown(report)

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
