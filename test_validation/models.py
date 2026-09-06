"""Shared dataclass schema for the test-validation engine (TEP Phase 5c).

Records what actually happened when an agent-authored test file was
executed: exit code, captured output, pass/fail, duration. No claim of
sandboxing beyond a process-level timeout -- see validation_runner.py.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

SCHEMA_VERSION = "1.0"


@dataclass
class ValidationOutcome:
    __test__ = False  # not a pytest test class, despite the name prefix

    test_file: str
    framework: str | None
    command: list[str]
    exit_code: int | None
    passed: bool
    timed_out: bool
    stdout_excerpt: str
    stderr_excerpt: str
    duration_ms: int


@dataclass
class ValidationStats:
    __test__ = False  # not a pytest test class, despite the name prefix

    test_files_considered: int
    passed: int
    failed: int
    timed_out: int


@dataclass
class ValidationReport:
    __test__ = False  # not a pytest test class, despite the name prefix

    schema_version: str
    repo_root: str
    generated_tests_dir: str
    test_environment_profile_path: str
    stats: ValidationStats
    outcomes: list[ValidationOutcome] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "ValidationReport":
        known = set(ValidationReport.__dataclass_fields__)
        raw = {k: v for k, v in data.items() if k in known}
        raw["stats"] = ValidationStats(**raw["stats"])
        raw["outcomes"] = [ValidationOutcome(**o) for o in raw.get("outcomes", [])]
        return ValidationReport(**raw)
