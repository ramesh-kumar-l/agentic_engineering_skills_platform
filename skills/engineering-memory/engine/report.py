"""Orchestrates ci-report-load -> memory-bank-parse -> module-resolution
-> relevance-scoring -> staleness-classification -> stats into the
deterministic MemoryQueryReport handed to the agent's Engineering Memory
Retrieval Checklist workflow (SKILL.md).
"""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .keyword_extractor import extract_keywords
from .memory_bank_parser import parse_decisions, parse_limitations
from .models import MemoryQueryReport, RelevanceMatch
from .module_resolver import resolve_module_mentions
from .relevance_scorer import score_relevance
from .staleness_classifier import classify_staleness
from .stats import compute_stats

# A record with zero keyword/module overlap never surfaces — fails closed
# toward precision, same discipline as every scorer in this portfolio
# except ADR-019's named inversion (which inverts for a different reason:
# content-inclusion cost, not retrieval-corpus noise).
_MIN_SCORE_THRESHOLD = 1


def build_report(
    task_description: str,
    ci_report_path: str,
    decisions_path: str,
    limitations_path: str,
    top_n: int = 10,
) -> MemoryQueryReport:
    ci_report = load_ci_report(ci_report_path)
    records = parse_decisions(decisions_path) + parse_limitations(limitations_path)

    warnings: list[str] = []
    if not task_description.strip():
        warnings.append("Task description is empty — no relevance scoring can be performed.")
    if not records:
        warnings.append(
            f"No records parsed from {decisions_path} / {limitations_path} — "
            "corpus is empty or the section-header format has drifted from what "
            "memory_bank_parser.py expects."
        )

    keywords = extract_keywords(task_description)
    matches: list[RelevanceMatch] = []
    for record in records:
        module_flags = resolve_module_mentions(record.mentioned_modules, ci_report)
        matched_module_count = sum(1 for f in module_flags if f.exists)
        score, matched_keywords = score_relevance(record, keywords, matched_module_count)
        if score < _MIN_SCORE_THRESHOLD:
            continue
        staleness = classify_staleness(record, module_flags)
        matches.append(
            RelevanceMatch(
                record=record,
                score=score,
                matched_keywords=matched_keywords,
                matched_modules=[f.module_path for f in module_flags if f.exists],
                module_flags=module_flags,
                staleness=staleness,
            )
        )

    matches.sort(key=lambda m: m.score, reverse=True)
    matches = matches[:top_n]

    stats = compute_stats(records, matches)

    return MemoryQueryReport(
        task_description=task_description,
        matches=matches,
        stats=stats,
        warnings=warnings,
    )
