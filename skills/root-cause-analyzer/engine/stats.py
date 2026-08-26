"""Objective, non-judgmental stats about a symptom description."""

from __future__ import annotations

import re

from .models import StackFrame, SymptomFlag, SymptomStats

_WORD = re.compile(r"\b\w+\b")


def compute_stats(
    symptom_text: str, flags: list[SymptomFlag], stack_frames: list[StackFrame]
) -> SymptomStats:
    return SymptomStats(
        word_count=len(_WORD.findall(symptom_text)),
        vague_symptom_count=sum(1 for f in flags if f.category == "vague-symptom"),
        stack_frame_count=len(stack_frames),
    )
