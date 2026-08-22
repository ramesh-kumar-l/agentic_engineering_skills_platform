"""Applies the risk pattern table to added lines in a DiffContext."""

from __future__ import annotations

from .models import DiffContext, RiskFlag
from .risk_patterns import PATTERNS

_REDACTED_PLACEHOLDER = "<redacted>"


def scan(context: DiffContext) -> list[RiskFlag]:
    """Scans added lines for risk patterns.

    For redact=True patterns (secrets), the matched span is replaced in-place
    on the LineChange itself, not just in the RiskFlag — the raw diff content
    is part of the engine's output (JSON/Markdown reports), so leaving the
    literal secret in `line.content` would defeat the point of redaction.
    """
    flags: list[RiskFlag] = []
    for diff_file in context.files:
        file_label = diff_file.new_path or diff_file.old_path or "<unknown>"
        for hunk in diff_file.hunks:
            for line in hunk.lines:
                if line.kind != "add":
                    continue
                for pattern in PATTERNS:
                    if not pattern.regex.search(line.content):
                        continue
                    if pattern.redact:
                        matched_text = _REDACTED_PLACEHOLDER
                        # sub() (not search()+slice) so every occurrence of
                        # this pattern on the line is redacted, not just the
                        # first — a line with two secrets of the same shape
                        # would otherwise leak the second one.
                        line.content = pattern.regex.sub(_REDACTED_PLACEHOLDER, line.content)
                    else:
                        matched_text = line.content.strip()
                    flags.append(
                        RiskFlag(
                            pattern_id=pattern.pattern_id,
                            category=pattern.category,
                            severity=pattern.severity,
                            file=file_label,
                            line=line.new_lineno or 0,
                            description=pattern.description,
                            matched_text=matched_text,
                        )
                    )
    return flags
