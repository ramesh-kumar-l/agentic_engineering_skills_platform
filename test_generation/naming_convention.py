"""Deterministic naming-convention inference for a target repo (TEP Phase
5c). Reuses the exact "looks like a test file" heuristic already applied
independently across refactoring-safety's/regression-hunter's/release-
readiness' test_coverage_scanner.py, rather than reinventing file-pattern
detection -- this module only adds majority-vote pattern classification on
top of an already-established file-recognition heuristic.

Read-only against the target repo (unchanged rule). An explicit override
file short-circuits inference entirely -- the storage mechanism chosen for
this phase: the resolved convention is emitted in this run's own --out
report; a later run passes it back in via --naming-convention-file rather
than this engine caching anything itself.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import NamingConvention

_PLATFORM_DEFAULT = NamingConvention(
    pattern="test_*.py", example="test_foo.py", source="platform-default"
)

_EXAMPLES = {
    "test_*.py": "test_foo.py",
    "*_test.py": "foo_test.py",
    "*Test.java": "FooTest.java",
    "*Tests.java": "FooTests.java",
    "*Spec.kt": "FooSpec.kt",
}


class NamingConventionError(Exception):
    """Raised when an explicit --naming-convention-file is malformed."""


def _looks_like_test_file(rel_path: Path) -> bool:
    if any(part in ("test", "tests") for part in rel_path.parts):
        return True
    stem_lower = rel_path.stem.lower()
    if stem_lower.startswith("test_") or stem_lower.endswith("_test"):
        return True
    return rel_path.stem.endswith(("Test", "Tests", "Spec"))


def _classify(rel_path: Path) -> str | None:
    stem = rel_path.stem
    suffix = rel_path.suffix
    if suffix == ".py" and stem.lower().startswith("test_"):
        return "test_*.py"
    if suffix == ".py" and stem.lower().endswith("_test"):
        return "*_test.py"
    if suffix in (".java", ".kt") and stem.endswith("Test"):
        return "*Test.java"
    if suffix in (".java", ".kt") and stem.endswith("Tests"):
        return "*Tests.java"
    if suffix == ".kt" and stem.endswith("Spec"):
        return "*Spec.kt"
    return None


def load_naming_convention_override(path: str | Path) -> NamingConvention:
    p = Path(path)
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise NamingConventionError(
            f"cannot read naming-convention override at {p}: {exc}"
        ) from exc
    try:
        return NamingConvention(
            pattern=raw["pattern"], example=raw["example"], source="override"
        )
    except KeyError as exc:
        raise NamingConventionError(
            f"{p} is missing required field {exc} — not a naming-convention "
            "override file"
        ) from exc


def infer_naming_convention(repo_root: str) -> NamingConvention:
    counts: dict[str, int] = {}
    root = Path(repo_root)
    if root.exists():
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(root)
            if not _looks_like_test_file(rel):
                continue
            pattern = _classify(rel)
            if pattern:
                counts[pattern] = counts.get(pattern, 0) + 1

    if not counts:
        return _PLATFORM_DEFAULT

    best = max(counts, key=lambda k: counts[k])
    return NamingConvention(pattern=best, example=_EXAMPLES[best], source="inferred")
