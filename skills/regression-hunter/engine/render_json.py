"""Full-detail JSON rendering of a RegressionHunterReport."""

from __future__ import annotations

import dataclasses
import json

from .models import RegressionHunterReport


def render_json(report: RegressionHunterReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
