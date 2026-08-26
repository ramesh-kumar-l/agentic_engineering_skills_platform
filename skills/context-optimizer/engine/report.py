"""Orchestrates ci-report-load -> keyword extraction -> per-file relevance
scoring -> structural boost -> tiering -> budget selection -> stats into
the deterministic context-optimizer pre-decision report packet handed to
the agent's Context Optimization Checklist workflow (SKILL.md Step 3)."""

from __future__ import annotations

from .budget_selector import apply_budget, assign_relevance_tiers
from .ci_report_loader import load_ci_report
from .keyword_extractor import extract_keywords
from .models import ContextOptimizationReport, FileRelevance
from .relevance_scorer import score_relevance
from .size_estimator import estimate_tokens
from .stats import compute_stats
from .structural_booster import apply_structural_boost


def build_report(
    task_description: str, ci_report_path: str, budget_lines: int | None = None
) -> ContextOptimizationReport:
    ci_report = load_ci_report(ci_report_path)

    keywords = extract_keywords(task_description)

    warnings: list[str] = []
    if not task_description.strip():
        warnings.append("Task description is empty — no recommendations can be produced.")
    elif not keywords:
        warnings.append(
            "No meaningful keywords could be extracted from the task description "
            "(all words were stopwords or shorter than 3 characters) — no "
            "recommendations can be produced."
        )
    ci_has_warning = not ci_report.files
    if ci_has_warning:
        warnings.append(
            "codebase-intelligence report declared zero files — no candidates "
            "can be scored. Reported explicitly, not silently returned as an "
            "empty-but-successful recommendation list."
        )

    candidates: list[FileRelevance] = []
    if keywords and not ci_has_warning:
        for file in ci_report.files:
            base_score, matched = score_relevance(file, keywords)
            score = apply_structural_boost(base_score, file.path, ci_report.dependency_graph)
            if score <= 0:
                continue
            candidates.append(
                FileRelevance(
                    path=file.path,
                    relevance_score=score,
                    matched_keywords=matched,
                    fan_in=ci_report.dependency_graph.fan_in.get(file.path, 0),
                    is_hotspot=file.path in ci_report.dependency_graph.hotspots,
                    line_count=file.line_count,
                    estimated_tokens=estimate_tokens(file.line_count),
                )
            )

    assign_relevance_tiers(candidates)
    apply_budget(candidates, budget_lines)

    stats = compute_stats(candidates)

    return ContextOptimizationReport(
        task_keywords=keywords, recommendations=candidates, stats=stats, warnings=warnings
    )
