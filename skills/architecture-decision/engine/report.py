"""Orchestrates ci-report-load -> option-parse -> scan -> impact-score ->
stats into the deterministic architecture-decision pre-decision report
packet."""

from __future__ import annotations

from .ci_report_loader import load_ci_report
from .decision_scanner import scan
from .impact_scorer import score_options
from .models import ArchitectureDecisionReport
from .option_parser import parse_options
from .stats import compute_stats


def build_report(decision_text: str, ci_report_path: str) -> ArchitectureDecisionReport:
    ci_report = load_ci_report(ci_report_path)
    options = parse_options(decision_text)
    flags = scan(decision_text)
    option_impacts = score_options(options, ci_report)
    stats = compute_stats(decision_text, options, flags)

    warnings: list[str] = []
    if not decision_text.strip():
        warnings.append("Decision description is empty.")
    if options and options[0].label == "proposed":
        warnings.append(
            "No explicit alternatives were parsed from the decision text — "
            "treating it as a single unlabeled option. If alternatives were "
            "actually considered, state them explicitly (e.g. 'Option A: ...')."
        )
    if not any(oi.impacted_modules for oi in option_impacts):
        warnings.append(
            "No modules in the codebase-intelligence report matched any "
            "option's keywords — blast radius could not be derived from "
            "real structural data for any option."
        )
    if any(oi.blast_radius_tier == "high" for oi in option_impacts):
        warnings.append(
            "At least one option's blast radius is HIGH (touches a hotspot "
            "or high fan-in module) — this decision likely warrants wider "
            "review before proceeding."
        )

    return ArchitectureDecisionReport(
        decision_text=decision_text,
        stats=stats,
        flags=flags,
        options=options,
        option_impacts=option_impacts,
        warnings=warnings,
    )
