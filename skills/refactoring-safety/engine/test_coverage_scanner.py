"""For a resolved target module, finds which modules in the
codebase-intelligence report look like tests that actually import it.

"Looks like a test" is a path-convention heuristic (a `tests/` directory
segment, or a filename starting with `test_`/ending in `_test`) — the same
kind of small, defensible, explicitly-heuristic table this project always
uses instead of claiming a stronger signal (e.g. actually running the test
suite) than a static report can support. A target with real callers but no
matching test module is exactly the situation safety_scorer.py escalates:
structurally consequential *and* unverified.
"""

from __future__ import annotations

from pathlib import PurePosixPath

from .models import CiReportContext


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
        if target_stem in imports_text or resolved_module_path.lower() in imports_text:
            covering.append(module.path)
    return covering
