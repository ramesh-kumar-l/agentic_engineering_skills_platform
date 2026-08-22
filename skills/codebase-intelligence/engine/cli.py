"""Thin CLI entry point. All real logic lives in report.py and the renderers.

Usage:
    python -m engine.cli <path> [--format json|markdown|both] [--out DIR]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .render_json import render_json
from .render_markdown import render_markdown
from .report import build_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="codebase-intelligence", description=__doc__)
    parser.add_argument("path", type=Path, help="Path to the repository to analyze")
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    parser.add_argument("--out", type=Path, default=None,
                         help="Directory to write report files into (default: stdout)")
    args = parser.parse_args(argv)

    if not args.path.exists():
        print(f"error: path does not exist: {args.path}", file=sys.stderr)
        return 1

    report = build_report(args.path)

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["report.md"] = render_markdown(report)

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
