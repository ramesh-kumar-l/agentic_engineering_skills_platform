"""Scans one ChangedFile's diff hunks for regression_patterns.py's
mechanically-detectable regression signals (ADR-015, Axis 1).

Four independent checks, each producing zero or more RegressionFlags:
1. line-shape patterns (removed exception handling / removed conditional
   guard) — per hunk, a removed line matching the pattern with no
   equivalent added line in the same hunk.
2. large unreplaced deletion — a hunk that removes at least
   LARGE_DELETION_THRESHOLD lines and adds none.
3. decreased test assertions — only for a test-shaped changed file: more
   removed assert/expect lines than added ones, across the whole file.
4. modified function signature with no corresponding test-file change — a
   `def`/`function`/`func` line touched in this file, but no OTHER changed
   file in the same diff looks like this file's test file by naming
   convention. This is the one check that needs the full diff's file list,
   not just this file's own hunks — a diff-level fact, not a codebase-
   intelligence fact (that composition is Axis 2's job, not this one's).
"""

from __future__ import annotations

from .models import ChangedFile, RegressionFlag
from .regression_patterns import (
    LARGE_DELETION_THRESHOLD,
    LINE_PATTERNS,
    is_assertion_line,
    is_test_shaped_path,
    touches_def_line,
)


def _file_label(file: ChangedFile) -> str:
    return file.effective_path or file.old_path or file.new_path or "<unknown>"


def _scan_line_patterns(file: ChangedFile) -> list[RegressionFlag]:
    label = _file_label(file)
    flags: list[RegressionFlag] = []
    for hunk in file.hunks:
        for pattern in LINE_PATTERNS:
            added_matches = any(
                line.kind == "add" and pattern.regex.match(line.content)
                for line in hunk.lines
            )
            if added_matches:
                continue
            for line in hunk.lines:
                if line.kind != "remove" or not pattern.regex.match(line.content):
                    continue
                flags.append(
                    RegressionFlag(
                        pattern_id=pattern.pattern_id,
                        category=pattern.category,
                        severity=pattern.severity,
                        file=label,
                        line=line.old_lineno or 0,
                        description=pattern.description,
                        matched_text=line.content.strip(),
                    )
                )
    return flags


def _scan_large_deletions(file: ChangedFile) -> list[RegressionFlag]:
    label = _file_label(file)
    flags: list[RegressionFlag] = []
    for hunk in file.hunks:
        removed = [line for line in hunk.lines if line.kind == "remove"]
        added = [line for line in hunk.lines if line.kind == "add"]
        if added or len(removed) < LARGE_DELETION_THRESHOLD:
            continue
        first_line = removed[0].old_lineno or 0
        flags.append(
            RegressionFlag(
                pattern_id="large-deletion-no-addition",
                category="diff-pattern",
                severity="medium",
                file=label,
                line=first_line,
                description=(
                    f"{len(removed)} lines removed in one hunk with zero "
                    "lines added — a large deletion with no replacement "
                    "code may drop behavior this file used to provide."
                ),
                matched_text=removed[0].content.strip(),
            )
        )
    return flags


def _scan_test_assertions(file: ChangedFile) -> list[RegressionFlag]:
    label = _file_label(file)
    if not is_test_shaped_path(label):
        return []
    removed_count = 0
    added_count = 0
    first_removed_line = 0
    for hunk in file.hunks:
        for line in hunk.lines:
            if line.kind == "remove" and is_assertion_line(line.content):
                removed_count += 1
                if not first_removed_line:
                    first_removed_line = line.old_lineno or 0
            elif line.kind == "add" and is_assertion_line(line.content):
                added_count += 1
    if removed_count <= added_count:
        return []
    return [
        RegressionFlag(
            pattern_id="decreased-test-assertions",
            category="diff-pattern",
            severity="high",
            file=label,
            line=first_removed_line,
            description=(
                f"{removed_count} assertion line(s) removed vs. "
                f"{added_count} added in this test file — real verification "
                "coverage may have decreased, not just been refactored."
            ),
            matched_text="",
        )
    ]


def _scan_signature_change_without_test_update(
    file: ChangedFile, all_files: list[ChangedFile]
) -> list[RegressionFlag]:
    label = _file_label(file)
    if is_test_shaped_path(label):
        return []

    touched_def_line = None
    for hunk in file.hunks:
        for line in hunk.lines:
            if line.kind in ("add", "remove") and touches_def_line(line.content):
                touched_def_line = line.old_lineno or line.new_lineno or 0
                break
        if touched_def_line is not None:
            break
    if touched_def_line is None:
        return []

    from pathlib import PurePosixPath

    stem = PurePosixPath(label).stem.lower()
    for other in all_files:
        if other is file:
            continue
        other_label = _file_label(other)
        if other_label is None or not is_test_shaped_path(other_label):
            continue
        other_stem = PurePosixPath(other_label).stem.lower()
        if stem in other_stem or stem == other_stem.removeprefix("test_").removesuffix("_test"):
            return []

    return [
        RegressionFlag(
            pattern_id="modified-signature-no-test-change",
            category="diff-pattern",
            severity="medium",
            file=label,
            line=touched_def_line,
            description=(
                "A function/method definition line was changed in this "
                "diff, but no other changed file in the same diff looks "
                "like this file's test file by naming convention — callers "
                "relying on the old signature may not be exercised by any "
                "test change in this diff."
            ),
            matched_text="",
        )
    ]


def scan(file: ChangedFile, all_files: list[ChangedFile]) -> list[RegressionFlag]:
    flags: list[RegressionFlag] = []
    flags.extend(_scan_line_patterns(file))
    flags.extend(_scan_large_deletions(file))
    flags.extend(_scan_test_assertions(file))
    flags.extend(_scan_signature_change_without_test_update(file, all_files))
    return flags
