"""Computes summary counts for a scan pass."""

from __future__ import annotations

from .models import ActionFlag, GuardStats, PiiMatch, SecretMatch, SensitivePathMatch


def compute_stats(
    content_text: str,
    secrets: list[SecretMatch],
    pii: list[PiiMatch],
    sensitive_path_matches: list[SensitivePathMatch],
    action_flags: list[ActionFlag],
) -> GuardStats:
    return GuardStats(
        content_word_count=len(content_text.split()),
        secret_count=len(secrets),
        pii_count=len(pii),
        sensitive_path_count=len(sensitive_path_matches),
        action_flag_count=len(action_flags),
    )
