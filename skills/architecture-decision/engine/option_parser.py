"""Splits a free-text architecture-decision description into distinct
candidate options.

Three fixed shapes covered, same "small, defensible table" discipline as
every other pattern module in this project:
  1. Explicit "Option A:" / "Option 1 —" markers.
  2. Numbered or lettered list items ("1. ...", "a) ...").
  3. A single unmarked comparison sentence using "vs"/"versus"/" or ".

If none of these shapes match, the whole text is treated as a single,
unlabeled option ("proposed") — a decision that only ever considers one path
is exactly the kind of thing the Architecture Decision Record checklist
(project-memory-bank/05-evaluation-framework.md) should flag, not something
this parser should paper over by inventing options that were never stated.
"""

from __future__ import annotations

import re

from .models import DecisionOption

_OPTION_MARKER = re.compile(
    r"(?im)^\s*option\s+([a-z0-9]+)\s*[:\-—]\s*(.+)$"
)
_LIST_ITEM = re.compile(r"(?m)^\s*(?:[0-9]+|[a-zA-Z])[.\)]\s+(.+)$")
_VS_SPLIT = re.compile(r"(?i)\s+(?:vs\.?|versus)\s+")


def parse_options(decision_text: str) -> list[DecisionOption]:
    text = decision_text.strip()
    if not text:
        return []

    marker_matches = list(_OPTION_MARKER.finditer(text))
    if marker_matches:
        return [
            DecisionOption(label=f"Option {m.group(1)}", raw_text=m.group(2).strip())
            for m in marker_matches
        ]

    list_matches = list(_LIST_ITEM.finditer(text))
    if len(list_matches) >= 2:
        return [
            DecisionOption(label=f"Item {i + 1}", raw_text=m.group(1).strip())
            for i, m in enumerate(list_matches)
        ]

    first_line = text.splitlines()[0]
    vs_parts = [p.strip() for p in _VS_SPLIT.split(first_line) if p.strip()]
    if len(vs_parts) >= 2:
        return [
            DecisionOption(label=f"Alternative {i + 1}", raw_text=part)
            for i, part in enumerate(vs_parts)
        ]

    return [DecisionOption(label="proposed", raw_text=text)]
