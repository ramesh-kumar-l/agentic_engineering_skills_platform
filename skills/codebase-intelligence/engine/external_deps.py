"""Parses external (third-party) dependency manifests.

Stdlib-only by design: uses a small manual TOML scan instead of `tomllib`
so the engine works on Python 3.10+ without a version-dependent import.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

from .models import ExternalDependency

_REQUIREMENTS_LINE = re.compile(r"^([A-Za-z0-9_.\-]+)\s*([<>=!~]=?[\w.\*]+)?")
_PYPROJECT_DEP_LINE = re.compile(r'^\s*"?([A-Za-z0-9_.\-]+)\s*([<>=!~]=?[\w.\*,\s]*)?"?\s*,?\s*$')


def parse_external_dependencies(root: Path) -> list[ExternalDependency]:
    deps: list[ExternalDependency] = []
    deps.extend(_parse_requirements_txt(root))
    deps.extend(_parse_pyproject_toml(root))
    deps.extend(_parse_package_json(root))
    return deps


def _parse_requirements_txt(root: Path) -> list[ExternalDependency]:
    path = root / "requirements.txt"
    if not path.exists():
        return []
    deps = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        match = _REQUIREMENTS_LINE.match(line)
        if match:
            deps.append(ExternalDependency(
                name=match.group(1), version=match.group(2), source_file="requirements.txt"
            ))
    return deps


def _parse_pyproject_toml(root: Path) -> list[ExternalDependency]:
    path = root / "pyproject.toml"
    if not path.exists():
        return []
    deps = []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    in_deps_block = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("dependencies") and "=" in stripped and "[" in stripped:
            in_deps_block = True
            continue
        if in_deps_block:
            if stripped.startswith("]"):
                in_deps_block = False
                continue
            match = _PYPROJECT_DEP_LINE.match(stripped)
            if match and match.group(1):
                deps.append(ExternalDependency(
                    name=match.group(1),
                    version=(match.group(2) or "").strip() or None,
                    source_file="pyproject.toml",
                ))
    return deps


def _parse_package_json(root: Path) -> list[ExternalDependency]:
    path = root / "package.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except (json.JSONDecodeError, OSError):
        return []
    deps = []
    for section in ("dependencies", "devDependencies"):
        for name, version in data.get(section, {}).items():
            deps.append(ExternalDependency(name=name, version=version, source_file="package.json"))
    return deps
