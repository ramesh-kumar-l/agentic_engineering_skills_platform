"""Lightweight, independent loader for a regression-hunter report.json —
extracts only each flagged file's diff-pattern flag descriptions, the
signal this engine grounds "regression-flag" scenarios in. Independent
copy convention, no cross-package import (ADR-010 lineage).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class RegressionFlagsError(Exception):
    """Raised when a path does not contain a valid regression-hunter report.json."""


@dataclass
class FlagSummary:
    pattern_id: str
    severity: str  # "low" | "medium" | "high"
    description: str


def load_regression_flags(path: str | Path) -> dict[str, list[FlagSummary]]:
    """Returns a mapping of file path -> its diff_pattern_flags, as FlagSummary."""
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RegressionFlagsError(
            f"cannot read regression-hunter report at {p}: {exc}"
        ) from exc

    try:
        files_raw = raw["files"]
    except KeyError as exc:
        raise RegressionFlagsError(
            f"{p} is missing required 'files' key — not a regression-hunter "
            "report.json"
        ) from exc

    flags_by_file: dict[str, list[FlagSummary]] = {}
    for entry in files_raw:
        try:
            file = entry["file"]
            flags_raw = entry["diff_pattern_flags"]
        except KeyError as exc:
            raise RegressionFlagsError(
                f"{p} has a file entry missing required field {exc} — "
                "not a regression-hunter report.json"
            ) from exc

        flags: list[FlagSummary] = []
        for f in flags_raw:
            try:
                flags.append(
                    FlagSummary(
                        pattern_id=f["pattern_id"],
                        severity=f["severity"],
                        description=f["description"],
                    )
                )
            except KeyError as exc:
                raise RegressionFlagsError(
                    f"{p} has a diff_pattern_flags entry missing required "
                    f"field {exc} — not a regression-hunter report.json"
                ) from exc
        flags_by_file[file] = flags

    return flags_by_file
