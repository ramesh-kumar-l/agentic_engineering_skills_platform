"""Pure detection functions: CiReportContext -> list[Finding].

Each detector reuses `external_dependencies` (and, for build systems only,
the already-scanned `files` list) rather than re-reading or re-parsing any
manifest file itself — the whole point of TEP Phase 3's exit criteria.
"""

from __future__ import annotations

from .ci_report_loader import CiExternalDependency, CiReportContext
from .models import Finding
from .signatures import (
    BUILD_SYSTEM_MANIFESTS,
    COVERAGE_TOOL_SIGNATURES,
    MOCK_FRAMEWORK_SIGNATURES,
    TEST_FRAMEWORK_SIGNATURES,
)


def _dep_keys(dep: CiExternalDependency) -> list[str]:
    """The full lowercased name, plus the artifact-id (after the last ':')
    for Maven/Gradle "group:artifact" coordinates — both checked for an
    exact signature match.
    """
    name_lower = dep.name.lower()
    keys = [name_lower]
    if ":" in name_lower:
        keys.append(name_lower.rsplit(":", 1)[-1])
    return keys


def _match_signatures(
    deps: list[CiExternalDependency], signatures: dict[str, str]
) -> list[Finding]:
    matches: dict[str, list[str]] = {}
    for dep in deps:
        for key in _dep_keys(dep):
            label = signatures.get(key)
            if label:
                matches.setdefault(label, []).append(dep.name)
    return [
        Finding(name=label, evidence=sorted(set(evidence)), confidence="dependency-confirmed")
        for label, evidence in matches.items()
    ]


def detect_test_frameworks(ctx: CiReportContext) -> list[Finding]:
    return _match_signatures(ctx.external_dependencies, TEST_FRAMEWORK_SIGNATURES)


def detect_mock_frameworks(ctx: CiReportContext) -> list[Finding]:
    return _match_signatures(ctx.external_dependencies, MOCK_FRAMEWORK_SIGNATURES)


def detect_coverage_tools(ctx: CiReportContext) -> list[Finding]:
    return _match_signatures(ctx.external_dependencies, COVERAGE_TOOL_SIGNATURES)


def detect_build_systems(ctx: CiReportContext) -> list[Finding]:
    manifests_with_deps = {dep.source_file for dep in ctx.external_dependencies}
    findings: list[Finding] = []
    for filename, label in BUILD_SYSTEM_MANIFESTS.items():
        if filename in manifests_with_deps:
            dep_names = sorted({d.name for d in ctx.external_dependencies if d.source_file == filename})
            findings.append(Finding(name=label, evidence=dep_names, confidence="dependency-confirmed"))
        elif filename in ctx.top_level_filenames:
            findings.append(Finding(name=label, evidence=[filename], confidence="manifest-only"))
    return findings
