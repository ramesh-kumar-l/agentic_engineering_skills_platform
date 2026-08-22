"""Loads a codebase-intelligence report.json into a lightweight local
CiReportContext — independent of the codebase-intelligence package itself
(no cross-package import), so this engine stays portable on its own.

A missing or malformed report is a hard failure, not a degraded path: see
project-memory-bank/11-decisions.md ADR-010. Grounding "affected files" in
real structural data is this skill's entire value proposition — proceeding
without it would let the agent fabricate plausible-looking file paths
instead of deriving them from real structure.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import CiDependencyGraph, CiModule, CiReportContext


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
        modules = [
            CiModule(
                path=m["path"],
                docstring=m.get("docstring"),
                functions=m.get("functions", []),
                classes=m.get("classes", []),
                imports=m.get("imports", []),
            )
            for m in raw["modules"]
        ]
        graph_raw = raw.get("dependency_graph", {})
        graph = CiDependencyGraph(
            fan_in=graph_raw.get("fan_in", {}),
            fan_out=graph_raw.get("fan_out", {}),
            hotspots=graph_raw.get("hotspots", []),
        )
        root_path = raw["root_path"]
    except KeyError as exc:
        raise CiReportError(
            f"codebase-intelligence report at {report_path} is missing expected "
            f"field {exc} — does not match the CodebaseIntelligenceReport schema."
        ) from exc

    return CiReportContext(root_path=root_path, modules=modules, dependency_graph=graph)
