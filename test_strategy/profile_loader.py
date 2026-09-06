"""Lightweight, independent loader for a project_intelligence
test-environment-profile.json — this engine's only environment-feasibility
substrate. Independent copy convention, no cross-package import (ADR-010
lineage): defines its own trimmed view rather than importing
project_intelligence's package internals.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


class ProfileLoadError(Exception):
    """Raised when a path does not contain a valid test-environment-profile.json."""


def _require_list(value, field_name: str, p: Path) -> list:
    if not isinstance(value, list):
        raise ProfileLoadError(
            f"{p} field {field_name!r} must be a list, got "
            f"{type(value).__name__} — not a test-environment-profile.json"
        )
    return value


@dataclass
class TestEnvironmentSummary:
    __test__ = False  # not a pytest test class, despite the name prefix

    repo_root: str
    primary_test_framework: str | None
    unavailable: list[str] = field(default_factory=list)


def load_test_environment_profile(path: str | Path) -> TestEnvironmentSummary:
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProfileLoadError(
            f"cannot read test-environment-profile at {p}: {exc}"
        ) from exc

    try:
        repo_root = raw["repo_root"]
        test_frameworks = raw["test_frameworks"]
        unavailable = raw["unavailable"]
    except KeyError as exc:
        raise ProfileLoadError(
            f"{p} is missing required field {exc} — not a "
            "test-environment-profile.json"
        ) from exc

    test_frameworks = _require_list(test_frameworks, "test_frameworks", p)
    unavailable = _require_list(unavailable, "unavailable", p)
    if test_frameworks and not isinstance(test_frameworks[0], dict):
        raise ProfileLoadError(
            f"{p} field 'test_frameworks[0]' must be an object, got "
            f"{type(test_frameworks[0]).__name__} — not a test-environment-profile.json"
        )

    primary_test_framework = test_frameworks[0]["name"] if test_frameworks else None

    return TestEnvironmentSummary(
        repo_root=repo_root,
        primary_test_framework=primary_test_framework,
        unavailable=unavailable,
    )
