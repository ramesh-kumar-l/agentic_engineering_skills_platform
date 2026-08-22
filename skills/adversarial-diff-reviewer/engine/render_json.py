"""Full-detail JSON rendering of a DiffIntelligenceReport."""

from __future__ import annotations

import dataclasses
import json

from .models import DiffIntelligenceReport


def render_json(report: DiffIntelligenceReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
