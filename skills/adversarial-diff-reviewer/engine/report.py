"""Orchestrator: assembles the deterministic pre-review packet (DiffIntelligenceReport)."""

from __future__ import annotations

from .diff_parser import parse_diff
from .models import DiffIntelligenceReport
from .risk_scanner import scan
from .stats import compute_stats


def build_report(diff_text: str) -> DiffIntelligenceReport:
    context = parse_diff(diff_text)
    flags = scan(context)
    stats = compute_stats(context)
    return DiffIntelligenceReport(
        stats=stats,
        risk_flags=flags,
        files=context.files,
        warnings=context.warnings,
    )
