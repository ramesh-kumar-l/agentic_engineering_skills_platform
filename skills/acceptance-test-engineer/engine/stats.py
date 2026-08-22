"""Objective, non-judgmental stats about a parsed requirement."""

from __future__ import annotations

import re

from .models import RequirementContext, RequirementStats, TestabilityFlag

_WORD = re.compile(r"\b\w+\b")
_NUMERIC = re.compile(r"\d+")
_EXISTING_CRITERIA_MARKER = re.compile(r"(?i)\b(given|when|then|acceptance criteria)\b")
_LIST_LINE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+", re.MULTILINE)


def compute_stats(
    context: RequirementContext, flags: list[TestabilityFlag]
) -> RequirementStats:
    return RequirementStats(
        sentence_count=len(context.sentences),
        word_count=len(_WORD.findall(context.raw_text)),
        vague_term_count=sum(1 for f in flags if f.category == "vague-term"),
        weak_modal_count=sum(1 for f in flags if f.category == "weak-modal"),
        numeric_quantifier_count=len(_NUMERIC.findall(context.raw_text)),
        existing_criteria_markers=(
            len(_EXISTING_CRITERIA_MARKER.findall(context.raw_text))
            + len(_LIST_LINE.findall(context.raw_text))
        ),
    )
