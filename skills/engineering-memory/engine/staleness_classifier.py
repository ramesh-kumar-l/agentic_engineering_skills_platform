"""Combines a record's own declared status with its resolved module flags
into one staleness signal, always attached to a match — never silently
dropped or silently trusted.

This is the direct, operational answer to A8's own named risk
(project-memory-bank/16-assumptions-and-validation.md): "stale/
unvalidated memory could actively degrade performance if treated as
authoritative." A stale-flagged match is still returned — an agent might
judge it still relevant despite the flag — but never presented as
equivalent to an ACTIVE, unflagged record.
"""

from __future__ import annotations

from .models import MemoryRecord, ModuleFlag, RecordStatus, StalenessFlag


def classify_staleness(record: MemoryRecord, module_flags: list[ModuleFlag]) -> StalenessFlag:
    if record.status == RecordStatus.FIXED:
        return StalenessFlag(
            is_stale=True, reason=f"{record.record_id} is marked FIXED in its own title."
        )
    if record.status == RecordStatus.SUPERSEDED:
        return StalenessFlag(
            is_stale=True, reason=f"{record.record_id} is marked SUPERSEDED in its own title."
        )

    missing = [f.module_path for f in module_flags if not f.exists]
    if module_flags and missing:
        return StalenessFlag(
            is_stale=True,
            reason=(
                f"{record.record_id} mentions module(s) no longer found in the "
                f"current codebase-intelligence report: {', '.join(missing)}."
            ),
        )
    return StalenessFlag(is_stale=False)
