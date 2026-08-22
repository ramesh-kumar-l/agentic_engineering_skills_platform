"""Orchestrates parse -> scan -> stats into the deterministic report packet."""

from __future__ import annotations

from .models import AcceptanceTestabilityReport
from .requirement_parser import parse_requirement
from .stats import compute_stats
from .testability_scanner import scan


def build_report(requirement_text: str) -> AcceptanceTestabilityReport:
    context = parse_requirement(requirement_text)
    flags = scan(context)
    stats = compute_stats(context, flags)

    warnings: list[str] = []
    if not context.sentences:
        warnings.append("No sentences parsed — requirement text may be empty or malformed.")

    return AcceptanceTestabilityReport(
        stats=stats,
        testability_flags=flags,
        sentences=context.sentences,
        warnings=warnings,
    )
