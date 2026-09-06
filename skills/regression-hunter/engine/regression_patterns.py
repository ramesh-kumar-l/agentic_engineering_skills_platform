"""Fixed table of mechanically-detectable diff-pattern regression signals —
Axis 1 of ADR-015's three-axis design (see project-memory-bank/11-
decisions.md). Scans the diff hunks THEMSELVES, not a free-text description
— this is what makes regression-hunter's deterministic layer different in
kind from every prior Pattern 2 skill's anti-pattern table (which scans
free text a human wrote), even though the "fixed table, leads not verdicts"
discipline (ADR-007) is identical.

Each pattern below flags a *candidate* for a behavioral regression risk, not
a verdict — a regex cannot know whether a removed `except` block was truly
load-bearing or dead code, only that removing exception handling is a shape
correlated with real regressions. The agent's Step 3 walk against the
Regression Risk Checklist (project-memory-bank/05-evaluation-framework.md)
is what actually judges whether a flagged change is a real risk.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class LinePattern:
    """A pattern matched against REMOVED lines within one hunk; cancelled if
    a line matching the same shape appears among that hunk's ADDED lines
    (replaced, not removed)."""

    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


LINE_PATTERNS: list[LinePattern] = [
    LinePattern(
        "removed-exception-handling", "diff-pattern", "high",
        re.compile(r"^\s*(except\b|catch\s*\()"),
        "An exception/catch handler was removed with no equivalent handler "
        "added in the same hunk — the error path it used to cover may now "
        "propagate unhandled or crash instead of degrading gracefully.",
    ),
    LinePattern(
        "removed-conditional-guard", "diff-pattern", "medium",
        re.compile(r"^\s*if\b"),
        "An `if` guard was removed with no equivalent guard added in the "
        "same hunk — code that used to be conditional may now always run, "
        "or vice versa.",
    ),
]

_ASSERTION_REGEX = re.compile(r"^\s*(assert\b|expect\s*\()")

# Hunk-level: a hunk that only deletes, with no matching addition, past this
# many removed lines is a large, unreplaced deletion.
LARGE_DELETION_THRESHOLD = 10

_DEF_LINE = re.compile(r"^\s*(def |function |func )\w")

# Java method signature -- requires an access modifier to keep false
# positives low (a disclosed miss: package-private methods with no
# modifier at all). Kotlin's `fun` is handled separately since it commonly
# carries its own modifier/override/suspend prefixes that don't fit
# _DEF_LINE's simple "keyword + space" shape.
_JVM_METHOD_LINE = re.compile(
    r"^\s*(?:public|private|protected)\s+"
    r"(?:static\s+|final\s+|abstract\s+|synchronized\s+|override\s+)*"
    r"[\w<>\[\],.?]+\s+\w+\s*\([^)]*\)\s*\{?\s*$"
)
_KOTLIN_FUN_LINE = re.compile(
    r"^\s*(?:public\s+|private\s+|internal\s+|protected\s+|override\s+|"
    r"suspend\s+|inline\s+|open\s+)*fun\s+\w"
)


def is_test_shaped_path(path: str) -> bool:
    """Same path-convention heuristic every test-coverage-aware module in
    this project uses (a `tests/` directory segment, or a `test_*`/`*_test`
    filename, or — ADR-022 — a JVM `*Test`/`*Tests`/`*Spec` suffix) — a
    small, defensible, explicitly-heuristic check, not a stronger claim
    than a static diff can support."""
    parts = PurePosixPath(path).parts
    if any(part in ("test", "tests") for part in parts):
        return True
    stem = PurePosixPath(path).stem
    stem_lower = stem.lower()
    if stem_lower.startswith("test_") or stem_lower.endswith("_test"):
        return True
    return stem.endswith(("Test", "Tests", "Spec"))


def touches_def_line(content: str) -> bool:
    return (
        bool(_DEF_LINE.match(content))
        or bool(_JVM_METHOD_LINE.match(content))
        or bool(_KOTLIN_FUN_LINE.match(content))
    )


def is_assertion_line(content: str) -> bool:
    return bool(_ASSERTION_REGEX.match(content))
