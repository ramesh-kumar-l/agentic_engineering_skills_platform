"""Orchestrates scan -> redact -> classify into the deterministic
SecurityGuardReport packet.

Composition with codebase-intelligence's report is OPTIONAL here (unlike
feature-planner's ADR-010) — this skill is a general-purpose classify/
sanitize/authorize gate useful standalone. A `--ci-report`, if given, only
adds an optional hotspot-touch note; a missing or unreadable report is a
warning, never a failure.
"""

from __future__ import annotations

import json

from .classification import classify
from .models import SecurityGuardReport
from .scanner import scan_action, scan_content, scan_paths
from .stats import compute_stats


def _hotspot_note(ci_report_path: str | None, paths: list[str]) -> list[str]:
    if not ci_report_path or not paths:
        return []
    try:
        with open(ci_report_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        hotspots = set(data["dependency_graph"]["hotspots"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError):
        return [f"Could not read optional --ci-report at {ci_report_path}; skipping hotspot annotation."]
    touched = sorted(set(paths) & hotspots)
    if touched:
        return [f"Touches known hotspot module(s) per codebase-intelligence: {', '.join(touched)}."]
    return []


def build_report(
    content_text: str,
    action_text: str = "",
    paths: list[str] | None = None,
    ci_report_path: str | None = None,
) -> SecurityGuardReport:
    paths = paths or []

    content_redacted, content_secrets, content_pii = scan_content(content_text)
    action_text_redacted, action_secrets, action_pii = scan_content(action_text)
    secrets = content_secrets + action_secrets
    pii = content_pii + action_pii
    sensitive_path_matches = scan_paths(paths)
    action_flags = scan_action(action_text)

    classification = classify(secrets, pii, sensitive_path_matches, action_flags, action_text, content_text)
    stats = compute_stats(content_text, secrets, pii, sensitive_path_matches, action_flags)

    warnings = _hotspot_note(ci_report_path, paths)
    if not content_text.strip() and not action_text.strip() and not paths:
        warnings.append("No content, action, or paths provided — nothing to classify.")

    return SecurityGuardReport(
        content_redacted=content_redacted,
        action_text_redacted=action_text_redacted,
        paths=paths,
        stats=stats,
        secrets=secrets,
        pii=pii,
        sensitive_paths=sensitive_path_matches,
        action_flags=action_flags,
        classification=classification,
        warnings=warnings,
    )
