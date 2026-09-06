"""Thin CLI entry point. All real logic lives in pipeline.py and staged_diff.py.

Chains the 6-stage TEP pipeline (codebase-intelligence -> regression-hunter ->
project_intelligence -> test_strategy -> scenario_planner -> test_generation)
into one call, seeded from a repo's staged git diff.

Usage:
    python -m engine.cli <target-repo-path> [--diff-file PATH] --out DIR

Diff text defaults to `git -C <target-repo-path> diff --staged`; pass
--diff-file to use a prior/synthetic diff instead. Set TEP_PLATFORM_ROOT to
this platform's checkout when invoking from an unrelated repo (e.g. once this
skill is installed into another repo's .claude/skills/) — it defaults to this
file's own checkout location otherwise.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .pipeline import PipelineStageError, run_pipeline
from .staged_diff import StagedDiffError, read_diff


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="test-case-generator", description=__doc__)
    parser.add_argument("repo_path", type=Path, help="Path to the target repo to analyze")
    parser.add_argument(
        "--diff-file", type=Path, default=None,
        help="Path to a unified-diff text file to use instead of `git diff --staged`",
    )
    parser.add_argument(
        "--out", type=Path, required=True,
        help="Directory to write all pipeline stage outputs into",
    )
    args = parser.parse_args(argv)

    if not args.repo_path.exists():
        print(f"error: path does not exist: {args.repo_path}", file=sys.stderr)
        return 1

    try:
        diff_text = read_diff(args.repo_path, args.diff_file)
    except StagedDiffError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    try:
        tg_report_path = run_pipeline(args.repo_path, diff_text, args.out)
    except PipelineStageError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    print(f"wrote {tg_report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
