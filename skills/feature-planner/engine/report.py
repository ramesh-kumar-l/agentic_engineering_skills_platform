"""Orchestrates ci-report-load -> scan -> relevance-score -> stats into the
deterministic feature-planning report packet."""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .models import FeaturePlanningReport
from .planning_scanner import scan
from .relevance_scorer import score_relevance
from .stats import compute_stats


def build_report(task_text: str, ci_report_path: str) -> FeaturePlanningReport:
    ci_report = load_ci_report(ci_report_path)
    flags = scan(task_text)
    stats = compute_stats(task_text, flags)
    relevance = score_relevance(task_text, ci_report)

    warnings: list[str] = []
    if not task_text.strip():
        warnings.append("Task description is empty.")
    if not relevance.scores:
        warnings.append(
            "No modules in the codebase-intelligence report matched the task "
            "description's keywords — affected files will have to be assumed, "
            "not derived from structure."
        )

    return FeaturePlanningReport(
        task_text=task_text,
        stats=stats,
        planning_flags=flags,
        relevance=relevance,
        warnings=warnings,
    )
