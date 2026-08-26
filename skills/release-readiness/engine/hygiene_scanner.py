"""Scans one ChangedFile's diff hunks for hygiene_patterns.py's
mechanically-detectable, release-blocking anti-patterns (ADR-016, Axis 1).

Two independent checks, each producing zero or more HygieneFlags:
1. added-line patterns (debug leftovers, TODO/FIXME/XXX markers,
   hardcoded-secret-shaped literals) — matched only against ADDED lines,
   same "flag what this diff introduces" discipline as
   adversarial-diff-reviewer's risk_scanner.py.
2. merge-conflict markers — matched against every line in every hunk
   (added, removed, or context), since a literal `<<<<<<<`/`=======`/
   `>>>>>>>` marker present anywhere in a hunk means the file is
   syntactically broken regardless of which side of the diff it's shown on.
"""

from __future__ import annotations

from .hygiene_patterns import ADDED_LINE_PATTERNS, CONFLICT_MARKER_REGEX
from .models import ChangedFile, HygieneFlag


def _file_label(file: ChangedFile) -> str:
    return file.effective_path or file.old_path or file.new_path or "<unknown>"


def _scan_added_line_patterns(file: ChangedFile) -> list[HygieneFlag]:
    label = _file_label(file)
    flags: list[HygieneFlag] = []
    for hunk in file.hunks:
        for line in hunk.lines:
            if line.kind != "add":
                continue
            for pattern in ADDED_LINE_PATTERNS:
                if not pattern.regex.search(line.content):
                    continue
                flags.append(
                    HygieneFlag(
                        pattern_id=pattern.pattern_id,
                        category=pattern.category,
                        severity=pattern.severity,
                        file=label,
                        line=line.new_lineno or 0,
                        description=pattern.description,
                        matched_text=line.content.strip(),
                    )
                )
    return flags


def _scan_conflict_markers(file: ChangedFile) -> list[HygieneFlag]:
    label = _file_label(file)
    flags: list[HygieneFlag] = []
    for hunk in file.hunks:
        for line in hunk.lines:
            if line.kind == "remove":
                continue
            if not CONFLICT_MARKER_REGEX.match(line.content):
                continue
            flags.append(
                HygieneFlag(
                    pattern_id="merge-conflict-marker",
                    category="merge-conflict-marker",
                    severity="high",
                    file=label,
                    line=line.new_lineno or line.old_lineno or 0,
                    description=(
                        "An unresolved merge-conflict marker "
                        "(<<<<<<<, =======, or >>>>>>>) is present in this "
                        "diff's post-image — the file is very likely "
                        "syntactically broken."
                    ),
                    matched_text=line.content.strip(),
                )
            )
    return flags


def scan(file: ChangedFile) -> list[HygieneFlag]:
    flags: list[HygieneFlag] = []
    flags.extend(_scan_added_line_patterns(file))
    flags.extend(_scan_conflict_markers(file))
    return flags
