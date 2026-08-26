"""Orchestrates the deterministic scan: builds DependencyRecords with pin
status, then runs the known-risk-name and duplicate-conflict detectors over
the raw CI-report dependency list.

License-risk detection is deliberately NOT implemented (see SKILL.md Known
Limitations): a manifest's own `license` field describes the project's OWN
license, not each dependency's license — per-dependency license data would
require inspecting installed package metadata, which this skill does not
do (no guarantee dependencies are installed, and doing so would mean this
skill silently depends on the target environment's install state). Shipping
a "license risk" flag without real per-dependency license data would be the
exact kind of ungrounded, plausible-looking-but-fabricated output this
project's ADR-010 discipline exists to prevent.
"""

from __future__ import annotations

from .duplicate_detector import find_duplicate_conflicts
from .models import CiExternalDependency, DependencyRecord, RiskFlag
from .pin_checker import classify_pin_status, is_unpinned
from .risk_patterns import match_known_risk


def build_dependency_records(dependencies: list[CiExternalDependency]) -> list[DependencyRecord]:
    return [
        DependencyRecord(
            name=dep.name,
            version=dep.version,
            source_file=dep.source_file,
            pin_status=classify_pin_status(dep.version),
        )
        for dep in dependencies
    ]


def scan(dependencies: list[CiExternalDependency]) -> tuple[list[DependencyRecord], list[RiskFlag]]:
    records = build_dependency_records(dependencies)
    flags: list[RiskFlag] = []

    for record in records:
        if is_unpinned(record.pin_status):
            severity = "high" if record.pin_status == "wildcard" else "low"
            flags.append(
                RiskFlag(
                    pattern_id=f"unpinned-{record.pin_status}",
                    category="unpinned-version" if record.pin_status != "wildcard" else "wildcard-version",
                    severity=severity,
                    dependency_name=record.name,
                    description=(
                        f"'{record.name}' has a {record.pin_status} version specifier "
                        f"({record.version!r}) — the exact resolved version is not "
                        "reproducible between installs."
                    ),
                    evidence=f"{record.source_file}: {record.version!r}",
                )
            )

        known_risk = match_known_risk(record.name)
        if known_risk is not None:
            flags.append(
                RiskFlag(
                    pattern_id="known-risk-name",
                    category="known-risk-name",
                    severity="medium",
                    dependency_name=record.name,
                    description=known_risk.reason,
                    evidence=f"{record.source_file}: {record.name}",
                )
            )

    flags.extend(find_duplicate_conflicts(dependencies))

    return records, flags
