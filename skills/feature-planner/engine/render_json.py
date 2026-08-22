"""Full-detail JSON rendering of a FeaturePlanningReport."""

from __future__ import annotations

import dataclasses
import json

from .models import FeaturePlanningReport


def render_json(report: FeaturePlanningReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
