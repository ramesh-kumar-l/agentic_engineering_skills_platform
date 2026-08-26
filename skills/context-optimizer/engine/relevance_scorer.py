"""Scores one CI file's relevance against a task's extracted keywords.

This is the FIFTH independent copy of a whole-token containment check
this project has now built to avoid arbitrary mid-word substring
collisions, in the L23/L24 lineage (project-memory-bank/
12-known-limitations.md) — after refactoring-safety's/regression-hunter's/
release-readiness's `target_resolver.py` (shipped with a bare substring
check, fixed later) and Phase 12's `location_resolver.py` (the first
built correct from day one, using a `\\bstem\\b` regex) — and the SECOND
built correct from day one, but using a genuinely different, disclosed
technique with a different precision/recall tradeoff than
`location_resolver.py`'s, not a copy-paste of it:

`location_resolver.py` uses a bare `\\bstem\\b` regex against a joined
string. `\\w` includes `_`, so that boundary never appears *inside* a
snake_case identifier — `\\bscanner\\b` correctly never matches inside
`testability_scanner_utils` (the exact L23 failure mode), but for the
same reason it would also never match `relevance_scorer.py` against the
keyword "relevance", since there is no `\\b` between `relevance` and
`_scorer` either. That strictness is the right choice for
`location_resolver.py`, which resolves to ONE canonical location and
where a false single-match attribution is expensive.

This scorer instead tokenizes both sides on `_`, `/`, `.`, and `-` (see
`keyword_extractor.tokenize`) and checks exact token-set membership. That
still blocks pure mid-word collisions with no boundary at all (a keyword
like "cat" still never matches inside "location", the same class of
protection `\\b` provides), but — deliberately, and differently from
`location_resolver.py` — it treats an underscore/slash/dot-delimited
compound identifier as multiple independent components, so a keyword can
match one real component of a compound filename (e.g. "resolver" against
`location_resolver.py`, or "scanner" against
`testability_scanner_utils.py`) even when that component is only part of
the full identifier. This is an accepted precision cost in exchange for
compound-identifier recall, appropriate here because this skill ranks
many weighted candidates rather than resolving to one canonical answer —
see SKILL.md Known Limitations for the disclosed consequence (a file can
surface on a component match even when that word isn't really what the
file is about).
"""

from __future__ import annotations

from .keyword_extractor import tokenize
from .models import CiFile

PATH_WEIGHT = 3
DOCSTRING_WEIGHT = 2
NAME_WEIGHT = 2
IMPORT_WEIGHT = 1


def score_relevance(file: CiFile, keywords: list[str]) -> tuple[int, list[str]]:
    """Returns (score, matched_keywords). A keyword contributes once per
    field it appears in (path/docstring/function+class names/imports),
    so a keyword matching in multiple fields is a stronger signal than
    one matching in only one."""
    path_tokens = set(tokenize(file.path))
    docstring_tokens = set(tokenize(file.docstring or ""))
    name_tokens = set(tokenize(" ".join(file.functions + file.classes)))
    import_tokens = set(tokenize(" ".join(file.imports)))

    score = 0
    matched: list[str] = []
    for kw in keywords:
        hit = False
        if kw in path_tokens:
            score += PATH_WEIGHT
            hit = True
        if kw in docstring_tokens:
            score += DOCSTRING_WEIGHT
            hit = True
        if kw in name_tokens:
            score += NAME_WEIGHT
            hit = True
        if kw in import_tokens:
            score += IMPORT_WEIGHT
            hit = True
        if hit:
            matched.append(kw)

    return score, matched
