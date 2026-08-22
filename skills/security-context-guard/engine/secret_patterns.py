"""Fixed table of mechanically-detectable secret/credential shapes.

These are *leads*, not verdicts — a regex hit does not mean a real secret
was exposed, and the absence of a hit does not mean the content is safe.
Every match is redacted (`pattern.regex.sub()`, every occurrence, not just
the first) before it ever reaches a model field, JSON, or Markdown output —
see scanner.py and project-memory-bank/11-decisions.md ADR-008 (established
for diff content) and ADR-011 (extends the same discipline here).
"""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SecretPattern:
    pattern_id: str
    severity: str
    regex: re.Pattern[str]
    description: str


PATTERNS: list[SecretPattern] = [
    SecretPattern(
        "generic-credential-assignment", "high",
        re.compile(
            r"(?i)\b(api[_-]?key|secret|password|passwd|token|"
            r"access[_-]?key)\b\s*[:=]\s*[\"']?[^\"'\s]{6,}[\"']?"
        ),
        "Looks like a hardcoded API key/secret/password/token assignment.",
    ),
    SecretPattern(
        "private-key-header", "high",
        re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "Private key material header found.",
    ),
    SecretPattern(
        "aws-access-key-id", "high",
        re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        "Looks like an AWS access key ID.",
    ),
    SecretPattern(
        "bearer-token", "medium",
        re.compile(r"(?i)\bbearer\s+[a-zA-Z0-9._-]{20,}\b"),
        "Looks like a bearer token.",
    ),
]
