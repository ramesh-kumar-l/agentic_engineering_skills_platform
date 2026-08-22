"""Orchestrates secret/PII/path/action scanning and redaction.

`scan_content()` is the single place raw text is ever touched — it returns
an already-redacted string plus match records that carry only a fixed
"<redacted>" placeholder, never the matched span. Callers (report.py) must
never hold onto the pre-redaction text after calling this.
"""

from __future__ import annotations

from . import action_patterns, pii_patterns, secret_patterns, sensitive_paths
from .models import ActionFlag, PiiMatch, SecretMatch, SensitivePathMatch

_REDACTED = "<redacted>"


def scan_content(text: str) -> tuple[str, list[SecretMatch], list[PiiMatch]]:
    redacted = text
    secrets: list[SecretMatch] = []
    for pattern in secret_patterns.PATTERNS:
        count = len(pattern.regex.findall(redacted))
        if count:
            secrets.extend(
                SecretMatch(pattern_id=pattern.pattern_id, severity=pattern.severity,
                            description=pattern.description)
                for _ in range(count)
            )
            # sub() (not search()+slice) so every occurrence on this text is
            # redacted, not just the first — see ADR-008's precedent.
            redacted = pattern.regex.sub(_REDACTED, redacted)

    pii: list[PiiMatch] = []
    for pattern in pii_patterns.PATTERNS:
        count = len(pattern.regex.findall(redacted))
        if count:
            pii.extend(
                PiiMatch(pattern_id=pattern.pattern_id, category=pattern.category,
                         description=pattern.description)
                for _ in range(count)
            )
            redacted = pattern.regex.sub(_REDACTED, redacted)

    return redacted, secrets, pii


def scan_paths(paths: list[str]) -> list[SensitivePathMatch]:
    return [
        SensitivePathMatch(path=path, pattern_id=pattern.pattern_id, description=pattern.description)
        for path, pattern in sensitive_paths.match_sensitive_paths(paths)
    ]


def scan_action(action_text: str) -> list[ActionFlag]:
    flags: list[ActionFlag] = []
    for pattern in action_patterns.PATTERNS:
        match = pattern.matches(action_text)
        if match:
            flags.append(
                ActionFlag(pattern_id=pattern.pattern_id, category=pattern.category,
                           description=pattern.description, matched_text=match.group(0))
            )
    return flags
