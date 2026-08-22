"""Deterministic sensitivity/verdict rollup.

`suggested_verdict` is always advisory — this module classifies and
recommends, it never authorizes anything itself (project-memory-bank/
06-security-model.md Human Approval principle; ADR-011). Defaults toward
REQUIRES_HUMAN_APPROVAL whenever evidence is inconclusive (no action
description given at all) — fail closed, not fail open.
"""

from __future__ import annotations

from .models import ActionFlag, Classification, PiiMatch, SecretMatch, SensitivePathMatch


def classify(
    secrets: list[SecretMatch],
    pii: list[PiiMatch],
    sensitive_path_matches: list[SensitivePathMatch],
    action_flags: list[ActionFlag],
    action_text: str,
    content_text: str,
) -> Classification:
    if secrets:
        sensitivity = "high"
    elif pii or sensitive_path_matches:
        sensitivity = "medium"
    elif content_text.strip():
        sensitivity = "low"
    else:
        sensitivity = "none"

    uncertain = not action_text.strip()

    evidence: list[str] = []
    if secrets:
        evidence.append(f"{len(secrets)} secret-shaped match(es).")
    if pii:
        evidence.append(f"{len(pii)} PII-shaped match(es).")
    if sensitive_path_matches:
        evidence.append(f"{len(sensitive_path_matches)} sensitive path match(es).")
    if action_flags:
        categories = sorted({flag.category for flag in action_flags})
        evidence.append(f"{len(action_flags)} high-risk action category match(es): {', '.join(categories)}.")
    if uncertain:
        evidence.append("No action description provided — cannot assess authorization requirement.")
    if not evidence:
        evidence.append("No secret/PII/sensitive-path/high-risk-action signal detected.")

    requires_approval = bool(secrets) or sensitivity in ("medium", "high") or bool(action_flags) or uncertain
    suggested_verdict = "REQUIRES_HUMAN_APPROVAL" if requires_approval else "AUTHORIZE"

    return Classification(
        sensitivity=sensitivity,
        suggested_verdict=suggested_verdict,
        evidence=evidence,
        uncertain=uncertain,
    )
