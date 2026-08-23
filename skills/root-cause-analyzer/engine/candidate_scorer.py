"""Deterministic candidate-location scoring: ranks codebase-intelligence
modules against a free-text symptom description using two evidence tiers.

Tier 1 — stack-trace evidence: a module whose path is directly named in a
parsed stack frame (stack_trace_parser.py) gets a flat, dominant score bonus
and `evidence_tier="stack-trace"`. This is real, mechanical evidence (a
runtime or a human actually wrote that path down), not an inference — it
always outranks a keyword-only match, same "grounded evidence beats guessed
plausibility" principle as feature-planner's fan-in/fan-out annotation
(project-memory-bank/11-decisions.md ADR-010).

Tier 2 — keyword overlap: identical weighting scheme to feature-planner's
relevance_scorer.py (path > name > docstring/imports), reused here rather
than reinvented, for the same reason ADR-007's engine+workflow split is
reused rather than redesigned per skill.

Neither tier is semantic understanding — see
project-memory-bank/12-known-limitations.md. A stack-trace hit tells you
where the failure *surfaced*, not necessarily where the defect *is*; a
keyword match tells you a module shares vocabulary with the symptom text,
not that it is actually involved. Both are leads for the agent's Step 3
investigation, not a diagnosis.
"""

from __future__ import annotations

import re

from .models import CandidateLocation, CandidateReport, CiReportContext, StackFrame

_WORD = re.compile(r"[a-zA-Z_][a-zA-Z0-9_]*")
_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "that",
    "this", "with", "is", "are", "be", "it", "as", "by", "at", "from",
    "when", "then", "after", "before", "then", "was", "were", "has", "have",
}
_MIN_KEYWORD_LEN = 3

_PATH_WEIGHT = 3
_NAME_WEIGHT = 2
_TEXT_WEIGHT = 1
_STACK_TRACE_BONUS = 100


def _extract_keywords(symptom_text: str) -> list[str]:
    words = (w.lower() for w in _WORD.findall(symptom_text))
    seen: list[str] = []
    for word in words:
        if len(word) < _MIN_KEYWORD_LEN or word in _STOPWORDS:
            continue
        if word not in seen:
            seen.append(word)
    return seen


def _stack_trace_hits(module_path: str, frames: list[StackFrame]) -> bool:
    normalized_module = module_path.replace("\\", "/")
    for frame in frames:
        normalized_frame = frame.path.replace("\\", "/")
        if normalized_frame == normalized_module or normalized_frame.endswith(
            "/" + normalized_module
        ):
            return True
    return False


def score_candidates(
    symptom_text: str, ci_report: CiReportContext, stack_frames: list[StackFrame]
) -> CandidateReport:
    keywords = _extract_keywords(symptom_text)
    candidates: list[CandidateLocation] = []

    for module in ci_report.modules:
        path_text = module.path.lower()
        name_text = " ".join(module.functions + module.classes).lower()
        rest_text = " ".join([module.docstring or "", *module.imports]).lower()

        matched: list[str] = []
        keyword_score = 0
        for keyword in keywords:
            hit = False
            if keyword in path_text:
                keyword_score += _PATH_WEIGHT
                hit = True
            if keyword in name_text:
                keyword_score += _NAME_WEIGHT
                hit = True
            if keyword in rest_text:
                keyword_score += _TEXT_WEIGHT
                hit = True
            if hit:
                matched.append(keyword)

        stack_hit = _stack_trace_hits(module.path, stack_frames)
        if keyword_score == 0 and not stack_hit:
            continue

        score = keyword_score + (_STACK_TRACE_BONUS if stack_hit else 0)
        fan_in = ci_report.dependency_graph.fan_in.get(module.path, 0)
        fan_out = ci_report.dependency_graph.fan_out.get(module.path, 0)
        is_hotspot = module.path in ci_report.dependency_graph.hotspots

        candidates.append(
            CandidateLocation(
                path=module.path,
                score=score,
                evidence_tier="stack-trace" if stack_hit else "keyword",
                matched_keywords=matched,
                stack_trace_hit=stack_hit,
                fan_in=fan_in,
                fan_out=fan_out,
                is_hotspot=is_hotspot,
            )
        )

    candidates.sort(key=lambda c: (-c.score, c.path))
    return CandidateReport(keywords=keywords, stack_frames=stack_frames, candidates=candidates)
