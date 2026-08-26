"""Parses this project's own project-memory-bank/ markdown into structured
MemoryRecords — the corpus engineering-memory retrieves against.

This is a SELF-REFERENTIAL composition (ADR-021): the primary input
corpus is this project's own 11-decisions.md and 12-known-limitations.md,
not a target repo's external artifacts. Only top-level `## ` section
headers are parsed — no front-matter or metadata schema exists in these
files, so this is intentionally a plain, disclosed regex walk over
section boundaries, not a general markdown AST.

`## L8 update:` style sub-entries are explicitly skipped — they are
status notes appended to L8's own entry (see 12-known-limitations.md),
not independent limitations with their own id. Treating them as
independent records would silently inflate the corpus with duplicates of
L8 under different bodies.
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import MemoryRecord, RecordStatus

_ADR_HEADER_RE = re.compile(r"^## (ADR-\d+):\s*(.+)$")
_LIMITATION_HEADER_RE = re.compile(r"^## L(\d+)(\s+update)?:\s*(.+)$")

# Matches a backtick-quoted `path/to/module.py` or `module.py` reference —
# the convention this memory bank already uses whenever an ADR or
# limitation names a real file. Deliberately does not try to detect a
# module name written in plain prose without backticks.
_CODE_SPAN_RE = re.compile(r"`([A-Za-z0-9_.\-/]*\.py)`")

_STATUS_RE = re.compile(r"\((FIXED|SUPERSEDED)[^)]*\)", re.IGNORECASE)


def _derive_status(title: str) -> RecordStatus:
    match = _STATUS_RE.search(title)
    if not match:
        return RecordStatus.ACTIVE
    word = match.group(1).upper()
    return RecordStatus.FIXED if word == "FIXED" else RecordStatus.SUPERSEDED


def _extract_mentioned_modules(body: str) -> list[str]:
    seen: list[str] = []
    for match in _CODE_SPAN_RE.finditer(body):
        token = match.group(1)
        if token not in seen:
            seen.append(token)
    return seen


def _parse_decision_sections(lines: list[str], source_file: str) -> list[MemoryRecord]:
    records: list[MemoryRecord] = []
    current_id: str | None = None
    current_title = ""
    current_line = 0
    current_body: list[str] = []

    def flush() -> None:
        if current_id is None:
            return
        body = "\n".join(current_body).strip()
        records.append(
            MemoryRecord(
                record_id=current_id,
                record_type="decision",
                title=current_title,
                body=body,
                source_file=source_file,
                source_line=current_line,
                status=_derive_status(current_title),
                mentioned_modules=_extract_mentioned_modules(body),
            )
        )

    for line_no, line in enumerate(lines, start=1):
        match = _ADR_HEADER_RE.match(line)
        if match is None:
            if current_id is not None:
                current_body.append(line)
            continue
        flush()
        current_id, current_title = match.group(1), match.group(2)
        current_line = line_no
        current_body = []

    flush()
    return records


def _parse_limitation_sections(lines: list[str], source_file: str) -> list[MemoryRecord]:
    records: list[MemoryRecord] = []
    current_id: str | None = None
    current_title = ""
    current_line = 0
    current_body: list[str] = []

    def flush() -> None:
        if current_id is None:
            return
        body = "\n".join(current_body).strip()
        records.append(
            MemoryRecord(
                record_id=current_id,
                record_type="limitation",
                title=current_title,
                body=body,
                source_file=source_file,
                source_line=current_line,
                status=_derive_status(current_title),
                mentioned_modules=_extract_mentioned_modules(body),
            )
        )

    for line_no, line in enumerate(lines, start=1):
        match = _LIMITATION_HEADER_RE.match(line)
        if match is None:
            if current_id is not None:
                current_body.append(line)
            continue
        flush()
        number, is_update, title_text = match.groups()
        if is_update:
            # An "## L8 update:" sub-entry — a status note, not an
            # independent record. Drop its body rather than attaching it
            # to any record.
            current_id = None
            current_title = ""
            current_body = []
            continue
        current_id, current_title = f"L{number}", title_text
        current_line = line_no
        current_body = []

    flush()
    return records


def parse_decisions(path: str | Path) -> list[MemoryRecord]:
    text = Path(path).read_text(encoding="utf-8")
    return _parse_decision_sections(text.splitlines(), str(path))


def parse_limitations(path: str | Path) -> list[MemoryRecord]:
    text = Path(path).read_text(encoding="utf-8")
    return _parse_limitation_sections(text.splitlines(), str(path))
