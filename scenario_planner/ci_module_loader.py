"""Lightweight, independent loader for a codebase-intelligence report.json
— extracts only each module's function/class name listing, the signal
this engine grounds "structural-listing" scenarios in. Independent copy
convention, no cross-package import (ADR-010 lineage): defines its own
trimmed view rather than importing codebase-intelligence's package
internals (same pattern regression-hunter's own CiModule already uses).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class CiModuleLoadError(Exception):
    """Raised when a path does not contain a valid codebase-intelligence report.json."""


@dataclass
class ModuleSummary:
    functions: list[str] = field(default_factory=list)
    classes: list[str] = field(default_factory=list)


def load_ci_modules(path: str | Path) -> dict[str, ModuleSummary]:
    """Returns a mapping of module path -> its function/class name listing."""
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CiModuleLoadError(
            f"cannot read codebase-intelligence report at {p}: {exc}"
        ) from exc

    try:
        modules_raw = raw["modules"]
    except KeyError as exc:
        raise CiModuleLoadError(
            f"{p} is missing required 'modules' key — not a "
            "codebase-intelligence report.json"
        ) from exc

    modules: dict[str, ModuleSummary] = {}
    for entry in modules_raw:
        try:
            modules[entry["path"]] = ModuleSummary(
                functions=entry.get("functions", []),
                classes=entry.get("classes", []),
            )
        except KeyError as exc:
            raise CiModuleLoadError(
                f"{p} has a module entry missing required field {exc} — "
                "not a codebase-intelligence report.json"
            ) from exc

    return modules
