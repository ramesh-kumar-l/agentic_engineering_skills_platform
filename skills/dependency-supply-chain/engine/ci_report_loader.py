"""Loads a codebase-intelligence report.json into a lightweight local
CiReportContext, extracting only the `external_dependencies` field this
engine needs — independent of the codebase-intelligence package itself
(no cross-package import), so this engine stays portable on its own.

A missing or malformed report is a hard failure, not a degraded path: see
project-memory-bank/11-decisions.md ADR-010 (reused a seventh time here).
Guessing at a project's real dependency list instead of using CI's real,
parsed data would be actively-harmful ungrounded output.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import CiExternalDependency, CiReportContext


class CiReportError(Exception):
    """Raised when a codebase-intelligence report.json is missing or malformed."""


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
        dependencies = [
            CiExternalDependency(
                name=d["name"], version=d.get("version"), source_file=d["source_file"]
            )
            for d in raw.get("external_dependencies", [])
        ]
        root_path = raw["root_path"]
    except KeyError as exc:
        raise CiReportError(
            f"codebase-intelligence report at {report_path} is missing expected "
            f"field {exc} — does not match the CodebaseIntelligenceReport schema."
        ) from exc

    return CiReportContext(root_path=root_path, dependencies=dependencies)
