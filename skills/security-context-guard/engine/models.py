"""Shared dataclass schema for the security-context-guard engine.

No field on `SecurityGuardReport` (or anything reachable from it) ever holds
a raw secret/PII value — `content_redacted` and `action_text_redacted` are
already-redacted by the time they reach this model (see scanner.py); every
match record carries only a fixed "<redacted>" placeholder, never the
matched span itself. See project-memory-bank/11-decisions.md ADR-008/ADR-011.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SecretMatch:
    pattern_id: str
    severity: str  # "low" | "medium" | "high"
    description: str
    redacted_snippet: str = "<redacted>"


@dataclass
class PiiMatch:
    pattern_id: str
    category: str  # "email" | "phone" | "ssn" | "credit-card"
    description: str
    redacted_snippet: str = "<redacted>"


@dataclass
class SensitivePathMatch:
    path: str
    pattern_id: str
    description: str


@dataclass
class ActionFlag:
    pattern_id: str
    category: str  # one of the six categories in project-memory-bank/06-security-model.md
    description: str
    matched_text: str  # the short keyword phrase matched, not user secret data


@dataclass
class Classification:
    sensitivity: str  # "none" | "low" | "medium" | "high"
    suggested_verdict: str  # "AUTHORIZE" | "REQUIRES_HUMAN_APPROVAL" — a lead, not a final decision
    evidence: list[str] = field(default_factory=list)
    uncertain: bool = False


@dataclass
class GuardStats:
    content_word_count: int
    secret_count: int
    pii_count: int
    sensitive_path_count: int
    action_flag_count: int


@dataclass
class SecurityGuardReport:
    """The deterministic classify/sanitize packet handed to the agent's
    Security Decision Checklist workflow (SKILL.md Step 3). The engine never
    authorizes anything itself — `classification.suggested_verdict` is
    advice, not an executed gate."""

    content_redacted: str
    action_text_redacted: str
    paths: list[str]
    stats: GuardStats
    secrets: list[SecretMatch] = field(default_factory=list)
    pii: list[PiiMatch] = field(default_factory=list)
    sensitive_paths: list[SensitivePathMatch] = field(default_factory=list)
    action_flags: list[ActionFlag] = field(default_factory=list)
    classification: Classification = field(
        default_factory=lambda: Classification(sensitivity="none", suggested_verdict="AUTHORIZE")
    )
    warnings: list[str] = field(default_factory=list)
