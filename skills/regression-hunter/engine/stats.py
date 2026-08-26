"""Objective, non-judgmental stats about a parsed diff plus its per-file
risk assessments."""

from __future__ import annotations

from .models import ChangedFile, FileRiskAssessment, RegressionStats


def _line_counts(file: ChangedFile) -> tuple[int, int]:
    added = 0
    removed = 0
    for hunk in file.hunks:
        for line in hunk.lines:
            if line.kind == "add":
                added += 1
            elif line.kind == "remove":
                removed += 1
    return added, removed


def compute_stats(
    files: list[ChangedFile], assessments: list[FileRiskAssessment]
) -> RegressionStats:
    lines_added = 0
    lines_removed = 0
    files_added = 0
    files_deleted = 0
    for file in files:
        added, removed = _line_counts(file)
        lines_added += added
        lines_removed += removed
        if file.is_new_file:
            files_added += 1
        if file.is_deleted_file:
            files_deleted += 1

    flag_count = sum(len(a.diff_pattern_flags) for a in assessments)
    high_risk_file_count = sum(1 for a in assessments if a.overall_risk_tier == "high")

    return RegressionStats(
        files_changed=len(files),
        files_added=files_added,
        files_deleted=files_deleted,
        lines_added=lines_added,
        lines_removed=lines_removed,
        flag_count=flag_count,
        high_risk_file_count=high_risk_file_count,
    )
