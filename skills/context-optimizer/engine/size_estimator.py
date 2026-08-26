"""Converts a real line_count (from the composed codebase-intelligence
report) into a crude estimated_tokens figure.

This is a deliberately rough, disclosed heuristic — a fixed
tokens-per-line multiplier, NOT a real tokenizer. This project makes no
network calls (project-memory-bank/11-decisions.md ADR-006), so no
`tiktoken`-class dependency is available or appropriate here; a real
tokenizer would also be language- and model-specific in a way a single
stdlib-only constant cannot be. `estimated_tokens` is order-of-magnitude
only and must never be read as an exact budget guarantee — stated in
SKILL.md Known Limitations, not discovered later.
"""

from __future__ import annotations

TOKENS_PER_LINE_ESTIMATE = 8


def estimate_tokens(line_count: int) -> int:
    return max(0, line_count) * TOKENS_PER_LINE_ESTIMATE
