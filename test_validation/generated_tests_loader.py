"""Lists agent-authored test files under a directory (TEP Phase 5c). No
cross-package import into test_generation -- this loader only needs a
directory of real files, not test_generation's plan/spec model.

Filters out anything that isn't a real candidate test source file: a real
dogfood run found pytest's own `.pytest_cache/` (created by a prior run in
the same directory) being listed as a "generated test," each producing a
bogus outcome. Recognized-extension + no-hidden/cache-directory-component
filtering avoids that without needing to know anything about naming
conventions.
"""

from __future__ import annotations

from pathlib import Path

_RECOGNIZED_SUFFIXES = {".py", ".java", ".kt"}


class GeneratedTestsError(Exception):
    """Raised when the generated-tests directory does not exist."""


def _is_real_candidate(path: Path, root: Path, resolved_root: Path) -> bool:
    if path.suffix not in _RECOGNIZED_SUFFIXES:
        return False
    rel_parts = path.relative_to(root).parts
    if any(part.startswith(".") or part == "__pycache__" for part in rel_parts):
        return False
    # A symlinked file, or a file reached through a symlinked ancestor
    # directory, can resolve outside `root` even though its own path
    # string looks contained -- reject anything that escapes on resolve.
    try:
        resolved = path.resolve(strict=True)
    except OSError:
        return False
    return resolved.is_relative_to(resolved_root)


def list_generated_tests(directory: str | Path, pattern: str = "*") -> list[Path]:
    d = Path(directory)
    if not d.is_dir():
        raise GeneratedTestsError(f"generated-tests directory not found: {d}")
    resolved_root = d.resolve()
    return sorted(
        p for p in d.rglob(pattern)
        if p.is_file() and _is_real_candidate(p, d, resolved_root)
    )
