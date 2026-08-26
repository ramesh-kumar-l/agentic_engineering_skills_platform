"""Turns a free-text task description into a deduplicated keyword list,
and exposes the same tokenizer relevance_scorer.py uses against each
memory record's title/body — using one shared tokenizer on both sides of
a match is what makes the comparison correct.

Duplicated from, not imported from, context-optimizer's own
keyword_extractor.py — skills in this portfolio stay independent
packages with no cross-skill imports (same convention every other
composing skill follows for its CI-report loader and similar shared
shapes).

`tokenize()` splits on any non-alphanumeric character, including `_`,
`/`, `.`, and `-` — deliberately more aggressive than a bare `\\b` regex
boundary, so a keyword like "resolver" matches a real filename component
(e.g. inside `module_resolver.py`) instead of only ever matching a whole
compound identifier.
"""

from __future__ import annotations

import re

_TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")

# Small, disclosed, non-exhaustive stopword list — same "fixed table, not
# NLP" discipline as every pattern table in this project.
_STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "to", "of", "in", "on", "for",
    "with", "is", "are", "was", "were", "be", "been", "being", "this",
    "that", "these", "those", "it", "its", "as", "at", "by", "from", "we",
    "our", "you", "your", "i", "not", "no", "do", "does", "did", "so",
    "if", "then", "than", "into", "about", "will", "would", "should",
    "can", "could", "have", "has", "had", "up", "out", "just", "also",
}

_MIN_KEYWORD_LENGTH = 3


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN_SPLIT_RE.split(text.lower()) if t]


def extract_keywords(task_description: str) -> list[str]:
    """Deduplicated, order-preserving keyword list: lowercased tokens,
    stopwords and sub-3-character tokens dropped. Literal keyword
    extraction, not NLP/semantic parsing (see SKILL.md Known Limitations)."""
    seen: list[str] = []
    for token in tokenize(task_description):
        if len(token) < _MIN_KEYWORD_LENGTH:
            continue
        if token in _STOPWORDS:
            continue
        if token not in seen:
            seen.append(token)
    return seen
