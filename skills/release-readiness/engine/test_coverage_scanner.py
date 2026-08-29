"""For a resolved changed file, finds which modules in the
codebase-intelligence report look like tests that actually import it.

Independent copy of refactoring-safety's/regression-hunter's
test_coverage_scanner.py pattern. "Looks like a test" is a path-convention
heuristic (a `tests/` directory segment, or a filename starting with
`test_`/ending in `_test`) — the same small, defensible, explicitly-
heuristic table this project always uses instead of claiming a stronger
signal (e.g. actually running the test suite) than a static report can
support.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from .models import CiReportContext


def _contains_whole_token(haystack: str, needle: str) -> bool:
    """Word-boundary-aware containment check.

    A bare `needle in haystack` substring check false-positives whenever
    `needle` (a module stem like "models") happens to appear inside a
    longer, unrelated identifier belonging to a different skill — see L24
    in project-memory-bank/12-known-limitations.md, which showed this
    corrupts `has_coverage` itself (a genuinely untested module can look
    "covered"), not just an inflated caller list. Since `\\w` includes `_`,
    a word-boundary match rejects same-stem collisions inside unrelated
    identifiers while still matching a real, dotted/path-qualified import.
    """
    if not needle:
        return False
    return re.search(rf"\b{re.escape(needle)}\b", haystack) is not None


def _looks_like_test_module(path: str) -> bool:
    parts = PurePosixPath(path).parts
    if any(part in ("test", "tests") for part in parts):
        return True
    stem = PurePosixPath(path).stem
    stem_lower = stem.lower()
    if stem_lower.startswith("test_") or stem_lower.endswith("_test"):
        return True
    # JVM convention: PascalCase suffix, case-sensitive (FooTest.java,
    # FooTests.kt, FooSpec.kt) -- case-sensitive specifically so this never
    # matches an unrelated lowercase stem like "manifest" (which lowercased
    # would spuriously end with "test").
    return stem.endswith(("Test", "Tests", "Spec"))


def find_test_coverage(resolved_module_path: str | None, ci_report: CiReportContext) -> list[str]:
    if resolved_module_path is None:
        return []

    target_stem = PurePosixPath(resolved_module_path).stem.lower()
    covering: list[str] = []
    for module in ci_report.modules:
        if not _looks_like_test_module(module.path):
            continue
        imports_text = " ".join(module.imports).lower()
        if _contains_whole_token(imports_text, target_stem) or _contains_whole_token(
            imports_text, resolved_module_path.lower()
        ):
            covering.append(module.path)
    return covering
