"""Full-detail JSON rendering of a SecurityGuardReport.

Safe by construction: every field on SecurityGuardReport is already
redacted/match-metadata-only by the time it reaches this renderer (see
models.py/scanner.py) — this module does not need its own redaction pass.
"""

from __future__ import annotations

import dataclasses
import json

from .models import SecurityGuardReport


def render_json(report: SecurityGuardReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
