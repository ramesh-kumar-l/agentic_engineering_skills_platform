# case-05-module-not-found

**Category**: staleness-module-missing

An ACTIVE-status record mentions a module (`engine/old_scanner.py`) that
no longer exists in the current codebase-intelligence report (only
`engine/new_scanner.py` is listed — a different basename, not a
containment collision). Exercises the second staleness path: module-gone,
not title-status-derived.
