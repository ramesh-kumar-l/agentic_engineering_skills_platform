"""Thin CLI entry point. All real logic lives in report.py and the renderers.

Usage:
    python -m engine.cli <content-file-or-'-'> [--action TEXT] \
        [--paths PATH [PATH ...]] [--ci-report report.json] \
        [--format json|markdown|both] [--out DIR]

Classifies content that is about to be exposed to a tool/agent/external
system, redacts any secret/PII matches found, and produces a
recommendation — never a self-executed authorization (see SKILL.md Security
Constraints / project-memory-bank/06-security-model.md).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .render_json import render_json
from .render_markdown import render_markdown
from .report import build_report


def _read_content_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="security-context-guard", description=__doc__)
    parser.add_argument(
        "path", help="Path to a content file to classify, or '-' to read from stdin."
    )
    parser.add_argument(
        "--action", default="",
        help="Free-text description of the action about to be taken with this content.",
    )
    parser.add_argument(
        "--paths", nargs="*", default=[],
        help="Paths involved in the action, checked against sensitive-path conventions.",
    )
    parser.add_argument(
        "--ci-report", default=None,
        help="Optional codebase-intelligence report.json — enriches hotspot annotation only; "
             "composition is optional here, unlike feature-planner's ADR-010.",
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

    content_text = _read_content_text(args.path)
    report = build_report(content_text, args.action, args.paths, args.ci_report)

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["security-guard-report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["security-guard-report.md"] = render_markdown(report)

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
