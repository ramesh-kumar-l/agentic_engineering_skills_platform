"""Detects the same dependency name declared with conflicting version
specifiers across more than one manifest (e.g. requirements.txt pins
`requests==2.28.0` while pyproject.toml declares `requests>=2.31`).

Deterministic: exact string comparison of the raw version specifiers per
manifest, case-insensitive on the dependency name (PyPI/npm names are
conventionally case-insensitive for matching purposes, even though the
`name` field itself is preserved as-declared elsewhere in the report).
"""

from __future__ import annotations

from collections import defaultdict

from .models import CiExternalDependency, RiskFlag


def find_duplicate_conflicts(dependencies: list[CiExternalDependency]) -> list[RiskFlag]:
    by_name: dict[str, list[CiExternalDependency]] = defaultdict(list)
    for dep in dependencies:
        by_name[dep.name.strip().lower()].append(dep)

    flags: list[RiskFlag] = []
    for lowered_name, group in by_name.items():
        distinct_versions = {(d.version or "").strip() for d in group}
        if len(group) < 2 or len(distinct_versions) < 2:
            continue
        sources = ", ".join(f"{d.source_file}={d.version or '(none)'}" for d in group)
        flags.append(
            RiskFlag(
                pattern_id="duplicate-conflicting-version",
                category="duplicate-version",
                severity="medium",
                dependency_name=group[0].name,
                description=(
                    f"'{group[0].name}' is declared with conflicting version "
                    "specifiers across multiple manifests."
                ),
                evidence=sources,
            )
        )
    return flags
