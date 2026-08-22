"""Deterministic keyword-overlap relevance scoring of codebase-intelligence
modules against a free-text task description.

This is a mechanical lead generator, not semantic understanding (see
project-memory-bank/12-known-limitations.md) — it can only surface modules
whose path/names/docstring/imports happen to share vocabulary with the task
text. The agent's Step 3 plan derivation is what actually decides which
files are truly affected; this layer exists so that decision is grounded in
real repo structure instead of guessed from scratch.
"""

from __future__ import annotations

import re

from .models import CiReportContext, RelevanceReport, RelevanceScore

_WORD = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "that",
    "this", "with", "is", "are", "be", "it", "as", "by", "at", "from",
    "should", "must", "will", "can", "add", "make", "when", "then",
}
_MIN_KEYWORD_LEN = 3

_PATH_WEIGHT = 3
_NAME_WEIGHT = 2
_TEXT_WEIGHT = 1


def _extract_keywords(task_text: str) -> list[str]:
    words = (w.lower() for w in _WORD.findall(task_text))
    seen: list[str] = []
    for word in words:
        if len(word) < _MIN_KEYWORD_LEN or word in _STOPWORDS:
            continue
        if word not in seen:
            seen.append(word)
    return seen


def score_relevance(task_text: str, ci_report: CiReportContext) -> RelevanceReport:
    keywords = _extract_keywords(task_text)
    scores: list[RelevanceScore] = []

    for module in ci_report.modules:
        path_text = module.path.lower()
        name_text = " ".join(module.functions + module.classes).lower()
        rest_text = " ".join([module.docstring or "", *module.imports]).lower()

        matched: list[str] = []
        score = 0
        for keyword in keywords:
            hit = False
            if keyword in path_text:
                score += _PATH_WEIGHT
                hit = True
            if keyword in name_text:
                score += _NAME_WEIGHT
                hit = True
            if keyword in rest_text:
                score += _TEXT_WEIGHT
                hit = True
            if hit:
                matched.append(keyword)

        if score == 0:
            continue

        fan_in = ci_report.dependency_graph.fan_in.get(module.path, 0)
        fan_out = ci_report.dependency_graph.fan_out.get(module.path, 0)
        is_hotspot = module.path in ci_report.dependency_graph.hotspots

        scores.append(
            RelevanceScore(
                path=module.path,
                score=score,
                matched_keywords=matched,
                fan_in=fan_in,
                fan_out=fan_out,
                is_hotspot=is_hotspot,
            )
        )

    scores.sort(key=lambda s: (-s.score, s.path))
    return RelevanceReport(keywords=keywords, scores=scores)
