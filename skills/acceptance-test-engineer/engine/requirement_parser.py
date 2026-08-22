"""Stdlib-only parser: free-text requirement -> structured RequirementContext.

Naive by design (see project-memory-bank/12-known-limitations.md): splits on
newlines first (so list/bullet items stay distinct sentences even without
terminal punctuation), then splits each line into sentences on '.', '!', '?'.
Abbreviations like "e.g." or "i.e." will over-split — acceptable for a
testability *lead* generator, not acceptable if this were claiming to be a
real NLP sentence boundary detector.
"""

from __future__ import annotations

import re

from .models import RequirementContext, RequirementSentence

_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+")
_LEADING_BULLET = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+")


def parse_requirement(text: str) -> RequirementContext:
    context = RequirementContext(raw_text=text)
    index = 0
    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = _LEADING_BULLET.sub("", raw_line.strip())
        if not line:
            continue
        for chunk in _SENTENCE_BOUNDARY.split(line):
            sentence = chunk.strip()
            if not sentence:
                continue
            context.sentences.append(
                RequirementSentence(index=index, text=sentence, source_line=line_no)
            )
            index += 1
    return context
