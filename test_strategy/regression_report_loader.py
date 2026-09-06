"""Lightweight, independent loader for a regression-hunter report.json —
this engine's only risk-signal substrate. Independent copy convention, no
cross-package import (ADR-010 lineage): this file defines its own trimmed
view of regression-hunter's output shape rather than importing
regression-hunter's package internals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class RegressionReportError(Exception):
    """Raised when a path does not contain a valid regression-hunter report.json."""


@dataclass
class RegressionFileAssessment:
    file: str
    is_new_file: bool
    is_deleted_file: bool
    overall_risk_tier: str  # "high" | "medium" | "low"
    has_test_coverage: bool
    flag_count: int


@dataclass
class RegressionReportContext:
    files: list[RegressionFileAssessment] = field(default_factory=list)


def load_regression_report(path: str | Path) -> RegressionReportContext:
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RegressionReportError(
            f"cannot read regression-hunter report at {p}: {exc}"
        ) from exc

    try:
        files_raw = raw["files"]
    except KeyError as exc:
        raise RegressionReportError(
            f"{p} is missing required 'files' key — not a regression-hunter report.json"
        ) from exc

    files: list[RegressionFileAssessment] = []
    for entry in files_raw:
        try:
            files.append(
                RegressionFileAssessment(
                    file=entry["file"],
                    is_new_file=entry["is_new_file"],
                    is_deleted_file=entry["is_deleted_file"],
                    overall_risk_tier=entry["overall_risk_tier"],
                    has_test_coverage=bool(
                        entry["test_coverage"]["test_coverage_modules"]
                    ),
                    flag_count=len(entry["diff_pattern_flags"]),
                )
            )
        except KeyError as exc:
            raise RegressionReportError(
                f"{p} has a file entry missing required field {exc} — "
                "not a regression-hunter report.json"
            ) from exc

    return RegressionReportContext(files=files)
