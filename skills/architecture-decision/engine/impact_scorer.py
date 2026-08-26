"""Deterministic blast-radius scoring: for each parsed decision option, ranks
codebase-intelligence modules by keyword relevance, then rolls that up into
a structural **blast-radius tier** using real fan-in/fan-out/hotspot data.

Keyword weighting is the same scheme reused across this project's judgment
skills (path > name > docstring/imports — feature-planner's
relevance_scorer.py, root-cause-analyzer's candidate_scorer.py), reused here
rather than reinvented.

What is genuinely new (ADR-013): the *point* of this scan is not "which
files does this option mention" but "how structurally consequential would
touching those files be" — a proposed option whose top matches are all
high-fan-in hotspot modules is a materially higher-risk decision than one
whose matches are leaf modules nobody else depends on, independent of how
many keywords matched. `blast_radius_score` sums `(fan_in + 1)` across the
matched modules (the `+1` so a zero-fan-in match still counts as touching
one module) and `hotspot_count` counts how many matched modules are already
flagged as hotspots by codebase-intelligence; `blast_radius_tier` rolls both
into one of three fixed bands so the agent's Step 3 checklist walk can reason
about risk without re-deriving it from raw numbers.
"""

from __future__ import annotations

import re

from .models import CiReportContext, DecisionOption, ImpactedModule, OptionImpact

_WORD = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "that",
    "this", "with", "is", "are", "be", "it", "as", "by", "at", "from",
    "we", "should", "will", "would", "option", "instead",
}
_MIN_KEYWORD_LEN = 3

_PATH_WEIGHT = 3
_NAME_WEIGHT = 2
_TEXT_WEIGHT = 1

_HIGH_BLAST_RADIUS = 10
_MEDIUM_BLAST_RADIUS = 3


def _extract_keywords(text: str) -> list[str]:
    words = (w.lower() for w in _WORD.findall(text))
    seen: list[str] = []
    for word in words:
        if len(word) < _MIN_KEYWORD_LEN or word in _STOPWORDS:
            continue
        if word not in seen:
            seen.append(word)
    return seen


def _blast_radius_tier(blast_radius_score: int, hotspot_count: int) -> str:
    if hotspot_count > 0 or blast_radius_score >= _HIGH_BLAST_RADIUS:
        return "high"
    if blast_radius_score >= _MEDIUM_BLAST_RADIUS:
        return "medium"
    return "low"


def score_option_impact(option: DecisionOption, ci_report: CiReportContext) -> OptionImpact:
    keywords = _extract_keywords(option.raw_text)
    impacted: list[ImpactedModule] = []

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

        impacted.append(
            ImpactedModule(
                path=module.path,
                relevance_score=score,
                matched_keywords=matched,
                fan_in=fan_in,
                fan_out=fan_out,
                is_hotspot=is_hotspot,
            )
        )

    impacted.sort(key=lambda m: (-m.relevance_score, m.path))

    blast_radius_score = sum(m.fan_in + 1 for m in impacted)
    hotspot_count = sum(1 for m in impacted if m.is_hotspot)

    return OptionImpact(
        option_label=option.label,
        option_text=option.raw_text,
        impacted_modules=impacted,
        blast_radius_score=blast_radius_score,
        hotspot_count=hotspot_count,
        blast_radius_tier=_blast_radius_tier(blast_radius_score, hotspot_count),
    )


def score_options(options: list[DecisionOption], ci_report: CiReportContext) -> list[OptionImpact]:
    return [score_option_impact(option, ci_report) for option in options]
