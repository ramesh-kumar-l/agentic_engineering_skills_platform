"""Loads an OPTIONAL regression-hunter report.json, if the caller supplied
one via --regression-report — surfaced verbatim as Axis 4 evidence, never
re-derived.

Unlike ci_report_loader.py (ADR-010, a hard precondition), this composition
is OPTIONAL, reusing security-context-guard's ADR-011 precedent: a missing
`--regression-report` flag is simply absent evidence, not a failure. A
*present but unreadable/malformed* report is a warning, not a hard failure
either — release-readiness's own assessment should not become unusable just
because a companion report happens to be stale or corrupt; the agent's Step
3 walk is told explicitly when this evidence is unavailable (see
report.py's warnings).
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import RegressionEvidence


def load_regression_evidence(
    path: str | Path | None,
) -> tuple[dict[str, RegressionEvidence], list[str]]:
    """Returns (per-file evidence keyed by the regression-hunter report's own
    `file` field, warnings). Empty dict + a warning if the path is given but
    unreadable/malformed. Empty dict + no warning if path is None (simply
    not supplied)."""
    if path is None:
        return {}, []

    report_path = Path(path)
    warnings: list[str] = []
    if not report_path.exists():
        return {}, [f"--regression-report path does not exist: {report_path} — evidence omitted, not a failure."]

    try:
        raw = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, [f"--regression-report at {report_path} is not valid JSON ({exc}) — evidence omitted, not a failure."]

    evidence: dict[str, RegressionEvidence] = {}
    for file_entry in raw.get("files", []):
        file_path = file_entry.get("file")
        if not file_path:
            continue
        flags = file_entry.get("diff_pattern_flags", [])
        evidence[file_path] = RegressionEvidence(
            available=True,
            overall_risk_tier=file_entry.get("overall_risk_tier"),
            diff_pattern_flag_count=len(flags),
            source_path=str(report_path),
        )

    if not evidence:
        warnings.append(
            f"--regression-report at {report_path} parsed but contained no "
            "per-file entries — evidence omitted, not a failure."
        )

    return evidence, warnings
