"""Resolves a knowledge candidate's evidence line against a real
codebase-intelligence report: does the narrative reference a real module,
and if so, is that module structurally significant (a hotspot / high
fan-in)?

This is the FOURTH independent copy of the word-boundary-aware containment
check first introduced (after the bug it fixes was found and disclosed
three times) in refactoring-safety's/regression-hunter's/release-
readiness's `target_resolver.py`, following project-memory-bank/
12-known-limitations.md L23/L24 — and the FIRST one built correct from the
start rather than shipped with the bare-substring bug and fixed later. A
bare `stem in text` containment check false-positives whenever a short
module stem happens to appear inside an unrelated word (the exact L23
failure mode: "scanner" matching inside "testability_scanner"); `\\bstem\\b`
does not, since `\\w` includes `_` and a boundary is required on both sides.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from .models import CiReportContext, ResolvedLocation

# Stems shorter than this are skipped entirely — a short/common module
# stem (e.g. "io", "cli") would otherwise match ordinary English words in
# a narrative far too often to be a meaningful signal. Disclosed in
# SKILL.md Known Limitations, not a silent gap.
_MIN_STEM_LENGTH = 4


def _stem(path: str) -> str:
    return PurePosixPath(path).stem


def _contains_whole_token(haystack: str, needle: str) -> bool:
    if not needle:
        return False
    return re.search(rf"\b{re.escape(needle)}\b", haystack) is not None


def resolve_mention(evidence_text: str, ci_report: CiReportContext) -> ResolvedLocation | None:
    """Returns the most structurally significant module whose stem appears
    as a whole word in `evidence_text`, or None if no module resolves.

    When more than one module's stem matches, the hotspot / highest-fan-in
    module wins — the same "don't let a coincidental match outrank a real
    structural signal" discipline location_resolver's sibling modules in
    other skills already apply to their own multi-candidate cases.
    """
    lowered = evidence_text.lower()
    matches = []
    for module in ci_report.modules:
        stem = _stem(module.path).lower()
        if len(stem) < _MIN_STEM_LENGTH:
            continue
        if _contains_whole_token(lowered, stem):
            matches.append(module)

    if not matches:
        return None

    def _rank(module):
        is_hotspot = module.path in ci_report.dependency_graph.hotspots
        fan_in = ci_report.dependency_graph.fan_in.get(module.path, 0)
        return (is_hotspot, fan_in)

    chosen = max(matches, key=_rank)
    return ResolvedLocation(
        module_path=chosen.path,
        fan_in=ci_report.dependency_graph.fan_in.get(chosen.path, 0),
        is_hotspot=chosen.path in ci_report.dependency_graph.hotspots,
    )
