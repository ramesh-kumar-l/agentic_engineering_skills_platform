"""Loads a codebase-intelligence report.json into a lightweight local
CiReportContext — independent of the codebase-intelligence package itself
(no cross-package import), following the exact pattern
`feature-planner/engine/ci_report_loader.py` already established
(project-memory-bank/11-decisions.md ADR-010).

A missing or malformed report is a hard failure, not a degraded path — this
phase's whole point is deriving the profile FROM real structural data, not
guessing when that data is absent.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class CiReportError(Exception):
    """Raised when a codebase-intelligence report.json is missing or malformed."""


@dataclass
class CiExternalDependency:
    name: str
    source_file: str


@dataclass
class CiReportContext:
    root_path: str
    language_breakdown: dict[str, int]
    external_dependencies: list[CiExternalDependency]
    top_level_filenames: list[str] = field(default_factory=list)


def load_ci_report(path: str | Path) -> CiReportContext:
    report_path = Path(path)
    if not report_path.exists():
        raise CiReportError(
            f"codebase-intelligence report not found at {report_path}. "
            "Run codebase-intelligence against the target repo first: "
            "python -m engine.cli <path> --format json --out <dir> "
            "(from skills/codebase-intelligence/)."
        )

    try:
        raw = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise CiReportError(
            f"codebase-intelligence report at {report_path} is not valid JSON: {exc}"
        ) from exc

    try:
        root_path = raw["root_path"]
        language_breakdown = raw["language_breakdown"]
        external_dependencies = [
            CiExternalDependency(name=d["name"], source_file=d["source_file"])
            for d in raw["external_dependencies"]
        ]
        top_level_filenames = [
            f["path"] for f in raw["files"] if "/" not in f["path"] and "\\" not in f["path"]
        ]
    except KeyError as exc:
        raise CiReportError(
            f"codebase-intelligence report at {report_path} is missing expected "
            f"field {exc} — does not match the CodebaseIntelligenceReport schema."
        ) from exc

    return CiReportContext(
        root_path=root_path,
        language_breakdown=language_breakdown,
        external_dependencies=external_dependencies,
        top_level_filenames=top_level_filenames,
    )
