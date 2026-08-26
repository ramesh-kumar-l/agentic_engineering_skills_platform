"""Loads a codebase-intelligence report.json into a lightweight local
CiReportContext — independent of the codebase-intelligence package itself
(no cross-package import), so this engine stays portable on its own.

A missing or malformed report is a hard failure, not a degraded path: see
project-memory-bank/11-decisions.md ADR-010, whose required-composition
pattern this skill reuses a NINTH time (Phase 13, after feature-planner,
root-cause-analyzer, architecture-decision, refactoring-safety,
regression-hunter, release-readiness, dependency-supply-chain, and
engineering-knowledge-capture). Guessing at which files are actually
relevant to a task, instead of resolving relevance against CI's real,
parsed file/module list, would be exactly the kind of ungrounded output
ADR-010 exists to prevent.

Every entry in CI's `files` list becomes a CiFile here (real line_count is
always present); the join against CI's separate `modules` list only
enriches a CiFile with docstring/functions/classes/imports when that file
was parseable — a file CI could not parse (or a non-code file that was
never a "module" at all) still gets a CiFile entry with real line_count
and an empty structural profile, so it is scored on path-keyword matching
alone rather than silently dropped from consideration.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import CiDependencyGraph, CiFile, CiReportContext


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
        file_rows = raw["files"]
        module_by_path = {m["path"]: m for m in raw["modules"]}
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

    files = []
    for f in file_rows:
        module = module_by_path.get(f["path"], {})
        files.append(
            CiFile(
                path=f["path"],
                line_count=f.get("line_count", 0),
                docstring=module.get("docstring"),
                functions=module.get("functions", []),
                classes=module.get("classes", []),
                imports=module.get("imports", []),
            )
        )

    return CiReportContext(root_path=root_path, files=files, dependency_graph=graph)
