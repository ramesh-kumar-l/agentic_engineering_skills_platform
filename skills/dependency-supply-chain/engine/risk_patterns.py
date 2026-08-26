"""A small, explicitly non-exhaustive curated table of package-name patterns
with a well-documented deprecation/abandonment history. This is NOT a live
vulnerability database — this project makes no network calls (stdlib-only,
offline, ADR-006) and has no CVE feed. Each entry names a specific, publicly
documented event so the flag is verifiable, not a vague "this might be bad."

Same disclaimer style as security-context-guard's secret/PII pattern
tables: leads for a human/agent to verify, never a verdict. A dependency NOT
appearing here is not thereby "safe" — absence of a match proves nothing.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class KnownRiskPattern:
    name_lower: str  # exact, lowercased package name to match
    ecosystem: str  # "python" | "npm" | "any"
    reason: str


KNOWN_RISK_PATTERNS: tuple[KnownRiskPattern, ...] = (
    KnownRiskPattern("distutils", "python", "Removed from the Python 3.12 standard library; migrate to setuptools/packaging."),
    KnownRiskPattern("nose", "python", "Unmaintained since 2015; the project itself recommends pytest or nose2."),
    KnownRiskPattern("request", "npm", "Deprecated by its maintainer in 2020; recommends node-fetch, axios, or undici."),
    KnownRiskPattern("left-pad", "npm", "Subject of the 2016 unpublish incident that broke a large share of the npm ecosystem; illustrative of unpinned-transitive-dependency risk, not a current threat."),
    KnownRiskPattern("event-stream", "npm", "A 2018 supply-chain compromise injected malicious code into a transitive dependency; kept as a historical example of why pin status and dependency provenance matter."),
)


def match_known_risk(name: str) -> KnownRiskPattern | None:
    lowered = name.strip().lower()
    for pattern in KNOWN_RISK_PATTERNS:
        if pattern.name_lower == lowered:
            return pattern
    return None
