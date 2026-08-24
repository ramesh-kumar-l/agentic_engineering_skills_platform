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

from pathlib import PurePosixPath

from .models import CiReportContext


def _looks_like_test_module(path: str) -> bool:
    parts = PurePosixPath(path).parts
    if any(part in ("test", "tests") for part in parts):
        return True
    stem = PurePosixPath(path).stem.lower()
    return stem.startswith("test_") or stem.endswith("_test")


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
