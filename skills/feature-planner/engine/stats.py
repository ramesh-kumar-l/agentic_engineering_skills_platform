"""Objective, non-judgmental stats about a task description."""

from __future__ import annotations

import re

from .models import PlanningFlag, TaskStats

_WORD = re.compile(r"\b\w+\b")


def compute_stats(task_text: str, flags: list[PlanningFlag]) -> TaskStats:
    return TaskStats(
        word_count=len(_WORD.findall(task_text)),
        vague_scope_count=sum(1 for f in flags if f.category == "vague-scope"),
        weak_modal_count=sum(1 for f in flags if f.category == "weak-goal-modal"),
    )
