"""Lightweight, independent loader for a test_strategy test-strategy-
report.json. Independent copy convention, no cross-package import (ADR-010
lineage): defines its own trimmed view rather than importing test_strategy's
package internals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class StrategyReportError(Exception):
    """Raised when a path does not contain a valid test-strategy-report.json."""


@dataclass
class TargetSummary:
    file: str
    priority: str  # "high" | "medium" | "low"
    generation_feasible: bool
    recommended_framework: str | None


@dataclass
class StrategyReportContext:
    repo_root: str
    targets: list[TargetSummary] = field(default_factory=list)


def load_strategy_report(path: str | Path) -> StrategyReportContext:
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise StrategyReportError(
            f"cannot read test-strategy report at {p}: {exc}"
        ) from exc

    try:
        repo_root = raw["repo_root"]
        targets_raw = raw["targets"]
    except KeyError as exc:
        raise StrategyReportError(
            f"{p} is missing required field {exc} — not a "
            "test-strategy-report.json"
        ) from exc

    targets: list[TargetSummary] = []
    for entry in targets_raw:
        try:
            targets.append(
                TargetSummary(
                    file=entry["file"],
                    priority=entry["priority"],
                    generation_feasible=entry["generation_feasible"],
                    recommended_framework=entry.get("recommended_framework"),
                )
            )
        except KeyError as exc:
            raise StrategyReportError(
                f"{p} has a target entry missing required field {exc} — "
                "not a test-strategy-report.json"
            ) from exc

    return StrategyReportContext(repo_root=repo_root, targets=targets)
