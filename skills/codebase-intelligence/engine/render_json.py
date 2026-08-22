"""Full-detail JSON rendering of a CodebaseIntelligenceReport.

This is the machine-readable output other skills should consume — it is
not truncated, unlike the Markdown renderer.
"""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import CodebaseIntelligenceReport


def render_json(report: CodebaseIntelligenceReport, indent: int = 2) -> str:
    return json.dumps(asdict(report), indent=indent, sort_keys=False)
