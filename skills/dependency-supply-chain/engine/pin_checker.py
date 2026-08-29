"""Classifies a declared dependency's version specifier into a pin-status
category. Deterministic, offline, no network — covers the ecosystems
codebase-intelligence's external_deps.py parses (Python pip-style
requirements/pyproject, npm-style package.json, and — via the `ecosystem`
param, ADR-022 — Maven pom.xml and Gradle build.gradle[.kts]).

Real risk this catches: a "range" or "wildcard" specifier means the exact
resolved version isn't reproducible between installs — a supply-chain
surface, not a cosmetic style issue (a compromised package release could be
silently picked up on the next `pip install`/`npm install`/build).
"""

from __future__ import annotations

import re

_WILDCARD_CHARS = ("*", "x", "X")
_RANGE_OPERATORS = ("<", ">", "~", "^", "!=", ",", "||")
_EXACT_PATTERN = re.compile(r"^={1,3}\s*[\w.\-]+$")
_BARE_VERSION_PATTERN = re.compile(r"^[0-9][\w.\-]*$")

# Maven version range, e.g. "[1.0,2.0)", "[1.5,)" — reproducibility-range,
# same category as pip's "range".
_MAVEN_RANGE = re.compile(r"^[\[(].*[\])]$")
# Gradle dynamic version, e.g. "31.+", "3.1.+" — same category as pip's
# wildcard.
_GRADLE_DYNAMIC = re.compile(r"(\+$|\.\+)")
# Unresolved Maven property placeholder, e.g. "${guava.version}" — a
# genuinely unknown literal value (this engine does not resolve properties),
# not a reproducibility-range problem, hence its own "unresolved" status.
_PROPERTY_PLACEHOLDER = re.compile(r"^\$\{[^}]+\}$")


def classify_pin_status(version: str | None, ecosystem: str = "generic") -> str:
    """Returns one of: "missing" | "wildcard" | "range" | "pinned" | "unresolved".

    `ecosystem` defaults to "generic" (pip/npm-style, the original behavior)
    for full backward compatibility. Pass "maven" or "gradle" for
    JVM-ecosystem-specific classification (ADR-022).
    """
    if version is None or version.strip() == "":
        return "missing"

    stripped = version.strip()

    if ecosystem in ("maven", "gradle"):
        if _PROPERTY_PLACEHOLDER.match(stripped):
            return "unresolved"
        if ecosystem == "maven" and _MAVEN_RANGE.match(stripped):
            return "range"
        if ecosystem == "gradle" and _GRADLE_DYNAMIC.search(stripped):
            return "wildcard"

    if any(ch in stripped for ch in _WILDCARD_CHARS):
        return "wildcard"

    if any(op in stripped for op in _RANGE_OPERATORS):
        return "range"

    if _EXACT_PATTERN.match(stripped) or _BARE_VERSION_PATTERN.match(stripped):
        return "pinned"

    return "range"


def is_unpinned(pin_status: str) -> bool:
    return pin_status in ("missing", "wildcard", "range", "unresolved")
