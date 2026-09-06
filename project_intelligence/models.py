"""The TestEnvironmentProfile schema for TEP Phase 3 (Project Intelligence
extensions).

Every finding is a list, not a single guessed value — a real repo can
legitimately mix ecosystems (e.g. a Python engine plus a JS frontend), and
picking one would hide the others. `confidence` distinguishes a finding
backed by an actual declared dependency ("dependency-confirmed") from one
inferred only from a manifest file's presence with no dependency entries
("manifest-only") — see [[20-test-environment-profile-schema]] for why that
distinction exists (`external_deps.py`'s known optional-dependencies gap,
[[12-known-limitations|L34]]).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA_VERSION = "1.0"


@dataclass
class Finding:
    name: str
    evidence: list[str] = field(default_factory=list)
    confidence: str = "dependency-confirmed"  # or "manifest-only"


@dataclass
class TestEnvironmentProfile:
    schema_version: str
    repo_root: str
    ci_report_path: str
    primary_language: str | None
    language_breakdown: dict[str, int]
    build_systems: list[Finding] = field(default_factory=list)
    test_frameworks: list[Finding] = field(default_factory=list)
    mock_frameworks: list[Finding] = field(default_factory=list)
    coverage_tools: list[Finding] = field(default_factory=list)
    android_test_frameworks: list[Finding] = field(default_factory=list)
    android_frameworks_absent: list[str] = field(default_factory=list)
    unavailable: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "TestEnvironmentProfile":
        known = set(TestEnvironmentProfile.__dataclass_fields__)
        raw = {k: v for k, v in data.items() if k in known}
        finding_list_keys = (
            "build_systems",
            "test_frameworks",
            "mock_frameworks",
            "coverage_tools",
            "android_test_frameworks",
        )
        for key in finding_list_keys:
            if key in raw:
                raw[key] = [Finding(**f) for f in raw[key]]
        return TestEnvironmentProfile(**raw)
