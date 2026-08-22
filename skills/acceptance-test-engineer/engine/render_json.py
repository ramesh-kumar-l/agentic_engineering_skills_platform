"""Full-detail JSON rendering of an AcceptanceTestabilityReport."""

from __future__ import annotations

import dataclasses
import json

from .models import AcceptanceTestabilityReport


def render_json(report: AcceptanceTestabilityReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
