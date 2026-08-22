"""Thin CLI entry point. All real logic lives in report.py and the renderers.

Usage:
    python -m engine.cli <requirement-file-or-'-'> [--format json|markdown|both] [--out DIR]

Reads free-text requirement/feature-description input from a file path or
stdin.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .render_json import render_json
from .render_markdown import render_markdown
from .report import build_report


def _read_requirement_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="acceptance-test-engineer", description=__doc__)
    parser.add_argument(
        "path", help="Path to a requirement text file, or '-' to read from stdin."
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

    requirement_text = _read_requirement_text(args.path)
    report = build_report(requirement_text)

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["acceptance-testability-report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["acceptance-testability-report.md"] = render_markdown(report)

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
