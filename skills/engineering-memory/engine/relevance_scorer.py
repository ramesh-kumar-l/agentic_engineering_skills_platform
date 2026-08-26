"""Scores one MemoryRecord's relevance against a task description's
extracted keywords, using whole-token set overlap — never substring
containment. See keyword_extractor.tokenize.

Title tokens are weighted higher than body tokens: a record whose TITLE
names the task's concept is a stronger signal than one that merely
mentions the same word somewhere in a long body. A resolved (existing)
module mention adds a further, separate boost — a record that names a
real module the task also touches is grounded in structure, not just
vocabulary overlap.
"""

from __future__ import annotations

from .keyword_extractor import tokenize
from .models import MemoryRecord

TITLE_WEIGHT = 3
BODY_WEIGHT = 1
MODULE_OVERLAP_WEIGHT = 2


def score_relevance(
    record: MemoryRecord, keywords: list[str], matched_module_count: int
) -> tuple[int, list[str]]:
    """Returns (score, matched_keywords). A keyword contributes once per
    field it appears in (title/body), so a keyword matching in both is a
    stronger signal than one matching in only one."""
    title_tokens = set(tokenize(record.title))
    body_tokens = set(tokenize(record.body))

    score = matched_module_count * MODULE_OVERLAP_WEIGHT
    matched: list[str] = []
    for kw in keywords:
        hit = False
        if kw in title_tokens:
            score += TITLE_WEIGHT
            hit = True
        if kw in body_tokens:
            score += BODY_WEIGHT
            hit = True
        if hit:
            matched.append(kw)

    return score, matched
