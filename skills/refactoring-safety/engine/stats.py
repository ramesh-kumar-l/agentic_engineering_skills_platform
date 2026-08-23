"""Objective, non-judgmental stats about a refactoring description."""

from __future__ import annotations

import re

from .models import RefactorStats, SafetyFlag, TargetAssessment

_WORD = re.compile(r"\b\w+\b")


def compute_stats(
    refactor_text: str,
    targets: list[TargetAssessment],
    flags: list[SafetyFlag],
) -> RefactorStats:
    resolved = sum(1 for t in targets if t.resolved_module_path is not None)
    return RefactorStats(
        word_count=len(_WORD.findall(refactor_text)),
        target_count=len(targets),
        resolved_target_count=resolved,
        flag_count=len(flags),
        high_severity_flag_count=sum(1 for f in flags if f.severity == "high"),
    )
