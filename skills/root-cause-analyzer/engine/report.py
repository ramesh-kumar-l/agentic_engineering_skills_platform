"""Orchestrates ci-report-load -> stack-trace-parse -> scan -> candidate-score
-> stats into the deterministic root-cause pre-investigation report packet."""

from __future__ import annotations

from .candidate_scorer import score_candidates
from .ci_report_loader import load_ci_report
from .models import RootCauseReport
from .stack_trace_parser import parse_stack_frames
from .stats import compute_stats
from .symptom_scanner import scan


def build_report(symptom_text: str, ci_report_path: str) -> RootCauseReport:
    ci_report = load_ci_report(ci_report_path)
    flags = scan(symptom_text)
    stack_frames = parse_stack_frames(symptom_text)
    stats = compute_stats(symptom_text, flags, stack_frames)
    candidates = score_candidates(symptom_text, ci_report, stack_frames)

    warnings: list[str] = []
    if not symptom_text.strip():
        warnings.append("Symptom description is empty.")
    if not candidates.candidates:
        warnings.append(
            "No modules in the codebase-intelligence report matched the symptom "
            "description's keywords or any parsed stack-trace path — candidate "
            "locations will have to be assumed, not derived from evidence."
        )
    if stack_frames and not any(c.stack_trace_hit for c in candidates.candidates):
        warnings.append(
            "Stack-trace frames were parsed from the symptom text but none of "
            "their paths matched a module in the codebase-intelligence report "
            "— the trace may reference a different repo, a vendored/third-party "
            "path, or a path outside this report's root."
        )

    return RootCauseReport(
        symptom_text=symptom_text,
        stats=stats,
        symptom_flags=flags,
        candidates=candidates,
        warnings=warnings,
    )
