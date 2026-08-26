"""Orchestrates ci-report-load -> narrative scan -> location resolution ->
priority scoring -> stats into the deterministic engineering-knowledge-
capture pre-decision report packet handed to the agent's Knowledge Capture
Checklist workflow (SKILL.md Step 3)."""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .knowledge_scanner import scan
from .location_resolver import resolve_mention
from .models import KnowledgeCaptureReport
from .priority_scorer import compute_priority
from .stats import compute_stats


def build_report(narrative_text: str, ci_report_path: str) -> KnowledgeCaptureReport:
    ci_report = load_ci_report(ci_report_path)

    warnings: list[str] = []
    if not narrative_text.strip():
        warnings.append("Narrative text is empty — no candidates can be extracted.")
    ci_has_warning = not ci_report.modules
    if ci_has_warning:
        warnings.append(
            "codebase-intelligence report declared zero modules — structural "
            "location resolution is impossible for any candidate; every "
            "candidate's priority fails closed to MEDIUM rather than being "
            "silently downranked to LOW."
        )

    candidates = scan(narrative_text)
    for candidate in candidates:
        resolved = None if ci_has_warning else resolve_mention(candidate.evidence, ci_report)
        if resolved is not None:
            candidate.resolved_module_path = resolved.module_path
            candidate.fan_in = resolved.fan_in
            candidate.is_hotspot = resolved.is_hotspot
        candidate.suggested_capture_priority = compute_priority(resolved, ci_has_warning)

    stats = compute_stats(candidates)

    return KnowledgeCaptureReport(candidates=candidates, stats=stats, warnings=warnings)
