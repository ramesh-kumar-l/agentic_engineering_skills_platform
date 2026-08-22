"""Computes objective diff statistics from a parsed DiffContext."""

from __future__ import annotations

from .models import DiffContext, DiffStats


def compute_stats(context: DiffContext) -> DiffStats:
    files_added = 0
    files_deleted = 0
    lines_added = 0
    lines_removed = 0
    hunk_count = 0

    for diff_file in context.files:
        if diff_file.is_new_file:
            files_added += 1
        if diff_file.is_deleted_file:
            files_deleted += 1
        hunk_count += len(diff_file.hunks)
        for hunk in diff_file.hunks:
            for line in hunk.lines:
                if line.kind == "add":
                    lines_added += 1
                elif line.kind == "remove":
                    lines_removed += 1

    return DiffStats(
        files_touched=len(context.files),
        files_added=files_added,
        files_deleted=files_deleted,
        lines_added=lines_added,
        lines_removed=lines_removed,
        hunk_count=hunk_count,
    )
