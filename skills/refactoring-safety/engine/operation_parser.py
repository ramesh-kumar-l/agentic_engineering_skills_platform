"""Parses a free-text refactoring description into an operation type and a
list of candidate target identifiers, before either is resolved against a
real codebase-intelligence report.

Operation detection: a small, defensible keyword table (same "fixed table,
not NLP" discipline as every other pattern module in this project) mapping
verb phrasing to one of eight fixed operation types, falling back to
"refactor" (generic) when no keyword matches — never guessing a more
specific type than the text actually supports.

Target extraction: backtick- or quote-wrapped identifiers are the highest-
confidence source (an author who names `foo.py` or `bar_function`
explicitly means it literally); when none are quoted, bare
snake_case/PascalCase/dotted identifiers are extracted as a fallback,
excluding common English words and the operation keywords themselves so
"rename the helper" doesn't extract "helper" as if it were as confident a
match as `` `helper.py` `` would have been — both remain named "targets";
resolution (whether they map to anything real) happens in
target_resolver.py, not here.
"""

from __future__ import annotations

import re

from .models import RefactorTarget

_OPERATION_KEYWORDS: list[tuple[str, re.Pattern[str]]] = [
    ("rename", re.compile(r"(?i)\brenam(?:e|ing|ed)\b")),
    ("delete", re.compile(r"(?i)\b(delet(?:e|ing|ed)|remov(?:e|ing|ed))\b")),
    ("move", re.compile(r"(?i)\bmov(?:e|ing|ed)\b")),
    ("change-signature", re.compile(
        r"(?i)\b(change|changing|changed)\s+(?:the\s+)?(?:signature|"
        r"parameters?|arguments?)\b"
    )),
    ("split", re.compile(r"(?i)\bsplit(?:ting)?\b")),
    ("merge", re.compile(r"(?i)\b(merg(?:e|ing|ed)|combin(?:e|ing|ed))\b")),
    ("extract", re.compile(r"(?i)\bextract(?:ing|ed)?\b")),
    ("inline", re.compile(r"(?i)\binlin(?:e|ing|ed)\b")),
]

_QUOTED_TARGET = re.compile(r"`([A-Za-z_][A-Za-z0-9_./]*)`|'([A-Za-z_][A-Za-z0-9_./]*)'")
_BARE_IDENTIFIER = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*\b")
_STOPWORDS = {
    "the", "a", "an", "to", "of", "in", "on", "for", "and", "or", "that",
    "this", "with", "is", "are", "be", "it", "as", "by", "at", "from",
    "we", "should", "will", "would", "into", "out", "so", "not", "its",
    "rename", "renaming", "renamed", "delete", "deleting", "deleted",
    "remove", "removing", "removed", "move", "moving", "moved", "change",
    "changing", "changed", "signature", "parameters", "parameter",
    "arguments", "argument", "split", "splitting", "merge", "merging",
    "combine", "combining", "extract", "extracting", "extracted",
    "inline", "inlining", "inlined", "function", "class", "module", "file",
    "method", "helper",
}
_MIN_IDENTIFIER_LEN = 3


def parse_operation_type(refactor_text: str) -> str:
    for op_type, pattern in _OPERATION_KEYWORDS:
        if pattern.search(refactor_text):
            return op_type
    return "refactor"


def _extract_quoted_targets(refactor_text: str) -> list[str]:
    names: list[str] = []
    for match in _QUOTED_TARGET.finditer(refactor_text):
        name = match.group(1) or match.group(2)
        if name and name not in names:
            names.append(name)
    return names


def _extract_bare_targets(refactor_text: str) -> list[str]:
    names: list[str] = []
    for match in _BARE_IDENTIFIER.finditer(refactor_text):
        word = match.group(0)
        lowered = word.lower()
        if len(word) < _MIN_IDENTIFIER_LEN or lowered in _STOPWORDS:
            continue
        # Require an underscore/dot, or an internal capital (camelCase) —
        # NOT a bare leading capital, which would misfire on ordinary
        # sentence-initial words like "Clean" in "Clean things up".
        looks_like_identifier = (
            "_" in word or "." in word or word[1:] != word[1:].lower()
        )
        if not looks_like_identifier:
            continue
        if word not in names:
            names.append(word)
    return names


def parse_targets(refactor_text: str) -> list[RefactorTarget]:
    quoted = _extract_quoted_targets(refactor_text)
    if quoted:
        return [RefactorTarget(name=name) for name in quoted]
    return [RefactorTarget(name=name) for name in _extract_bare_targets(refactor_text)]


def parse_operation(refactor_text: str) -> tuple[str, list[RefactorTarget]]:
    return parse_operation_type(refactor_text), parse_targets(refactor_text)
