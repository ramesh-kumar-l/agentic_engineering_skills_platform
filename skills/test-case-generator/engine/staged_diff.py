"""Resolves the diff text to feed regression-hunter: an explicit --diff-file,
or `git diff --staged` in the target repo when none is given.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


class StagedDiffError(Exception):
    pass


def read_diff(repo_path: Path, diff_file: Path | None) -> str:
    if diff_file is not None:
        return diff_file.read_text(encoding="utf-8", errors="replace")

    result = subprocess.run(
        ["git", "-C", str(repo_path), "diff", "--staged"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise StagedDiffError(f"git diff --staged failed: {result.stderr.strip()}")
    if not result.stdout.strip():
        raise StagedDiffError(
            "no staged changes in this repo (git diff --staged is empty) — "
            "stage a change with `git add` first, or pass --diff-file"
        )
    return result.stdout
