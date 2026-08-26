"""Classifies a declared dependency's version specifier into a pin-status
category. Deterministic, offline, no network — covers the two ecosystems
codebase-intelligence's external_deps.py parses (Python pip-style
requirements/pyproject, and npm-style package.json).

Real risk this catches: a "range" or "wildcard" specifier means the exact
resolved version isn't reproducible between installs — a supply-chain
surface, not a cosmetic style issue (a compromised package release could be
silently picked up on the next `pip install`/`npm install`).
"""

from __future__ import annotations

import re

_WILDCARD_CHARS = ("*", "x", "X")
_RANGE_OPERATORS = ("<", ">", "~", "^", "!=", ",", "||")
_EXACT_PATTERN = re.compile(r"^={1,3}\s*[\w.\-]+$")
_BARE_VERSION_PATTERN = re.compile(r"^[0-9][\w.\-]*$")


def classify_pin_status(version: str | None) -> str:
    """Returns one of: "missing" | "wildcard" | "range" | "pinned"."""
    if version is None or version.strip() == "":
        return "missing"

    stripped = version.strip()

    if any(ch in stripped for ch in _WILDCARD_CHARS):
        return "wildcard"

    if any(op in stripped for op in _RANGE_OPERATORS):
        return "range"

    if _EXACT_PATTERN.match(stripped) or _BARE_VERSION_PATTERN.match(stripped):
        return "pinned"

    return "range"


def is_unpinned(pin_status: str) -> bool:
    return pin_status in ("missing", "wildcard", "range")
