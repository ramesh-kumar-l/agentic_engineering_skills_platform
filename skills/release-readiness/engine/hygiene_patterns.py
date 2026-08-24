"""Fixed table of mechanically-detectable, release-blocking diff-hygiene
anti-patterns — Axis 1 of ADR-016's design (see project-memory-bank/11-
decisions.md).

Scans the diff hunks THEMSELVES, the same "scan the diff, not a free-text
description" approach regression-hunter's ADR-015 established. Unlike
regression-hunter's regression_patterns.py (which flags shapes correlated
with a REGRESSION in existing behavior), this table flags shapes that are
release blockers on their OWN terms, regardless of whether they change
behavior — a leftover debug statement, an unresolved merge-conflict marker,
or a hardcoded-secret-shaped literal are each reasons to block a release
even in an otherwise-correct diff.

These are *leads*, not verdicts (ADR-007) — a regex hit does not prove a
literal is a real secret (see the security-context-guard precedent this
table is an independent copy of, in miniature), and the absence of a hit
does not prove the diff is clean. The agent's Step 3 walk (Regression... no,
Release Readiness Checklist) treats a hygiene flag as an absolute blocker by
DESIGN (see readiness_scorer.py) precisely because these categories are
narrow and mechanical enough that a fixed table catches them reliably —
unlike regression/security judgment, which stays advisory.
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class HygienePattern:
    pattern_id: str
    category: str
    severity: str
    regex: re.Pattern[str]
    description: str


# Matched against ADDED lines only — a debug statement or TODO marker that
# was already present and untouched by this diff is not this diff's problem
# to flag.
ADDED_LINE_PATTERNS: list[HygienePattern] = [
    HygienePattern(
        "debug-print-leftover", "debug-leftover", "medium",
        re.compile(
            r"\bconsole\.log\s*\(|\bpdb\.set_trace\s*\(|"
            r"\bdebugger\s*;|\bbreakpoint\s*\(|^\s*print\s*\("
        ),
        "Debug statement (print/console.log/pdb/debugger/breakpoint) left "
        "in added code — likely leftover from local debugging, not intended "
        "for a released version.",
    ),
    HygienePattern(
        "todo-blocking-marker", "todo-blocking", "low",
        re.compile(r"(?:#|//)\s*(TODO|FIXME|XXX)\b"),
        "TODO/FIXME/XXX marker left in added code — may indicate "
        "intentionally incomplete work not yet ready to ship.",
    ),
    HygienePattern(
        "hardcoded-secret-shaped", "hardcoded-secret", "high",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|password|passwd|token|"
            r"access[_-]?key)\b\s*[:=]\s*[\"'][^\"']{6,}[\"']"
        ),
        "Line looks like a hardcoded secret/credential literal — an "
        "independent copy of security-context-guard's generic-credential-"
        "assignment pattern, in miniature; a lead, not proof of a real leak.",
    ),
]

# Matched against every line of the hunk (not just added) — a literal,
# unresolved merge-conflict marker present ANYWHERE in the diff's post-image
# means the file is syntactically broken, regardless of which side of the
# +/- it landed on in this particular hunk view.
CONFLICT_MARKER_REGEX = re.compile(r"^(<{7}|={7}|>{7})(\s|$)")
