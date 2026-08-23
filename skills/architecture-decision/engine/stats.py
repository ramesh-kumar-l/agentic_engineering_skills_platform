"""Objective, non-judgmental stats about a decision description."""

from __future__ import annotations

import re

from .models import DecisionFlag, DecisionOption, DecisionStats

_WORD = re.compile(r"\b\w+\b")


def compute_stats(
    decision_text: str, options: list[DecisionOption], flags: list[DecisionFlag]
) -> DecisionStats:
    return DecisionStats(
        word_count=len(_WORD.findall(decision_text)),
        option_count=len(options),
        flag_count=len(flags),
        high_severity_flag_count=sum(1 for f in flags if f.severity == "high"),
    )
