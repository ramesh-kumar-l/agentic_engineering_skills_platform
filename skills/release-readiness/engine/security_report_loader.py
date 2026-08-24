"""Loads an OPTIONAL security-context-guard report.json, if the caller
supplied one via --security-report — surfaced verbatim as Axis 5 evidence,
never re-derived.

security-context-guard's report classifies a single content/action blob
(`classification.sensitivity` / `classification.suggested_verdict`), not
per-diff-file — so this evidence is kept report-level on
ReleaseReadinessReport.security_evidence, not attached to individual files.
Same optional-composition discipline as regression_report_loader.py (ADR-011
precedent): missing flag -> simply absent, not a failure; present but
unreadable/malformed -> a warning, not a hard failure.
"""

from __future__ import annotations

import json
from pathlib import Path

from .models import SecurityEvidence


def load_security_evidence(path: str | Path | None) -> tuple[SecurityEvidence, list[str]]:
    if path is None:
        return SecurityEvidence(), []

    report_path = Path(path)
    if not report_path.exists():
        return SecurityEvidence(), [
            f"--security-report path does not exist: {report_path} — evidence omitted, not a failure."
        ]

    try:
        raw = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return SecurityEvidence(), [
            f"--security-report at {report_path} is not valid JSON ({exc}) — evidence omitted, not a failure."
        ]

    classification = raw.get("classification")
    if not isinstance(classification, dict):
        return SecurityEvidence(), [
            f"--security-report at {report_path} has no 'classification' field — "
            "evidence omitted, not a failure."
        ]

    return (
        SecurityEvidence(
            available=True,
            sensitivity=classification.get("sensitivity"),
            suggested_verdict=classification.get("suggested_verdict"),
            source_path=str(report_path),
        ),
        [],
    )
