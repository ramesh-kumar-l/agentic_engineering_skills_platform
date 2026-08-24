"""Full-detail JSON rendering of a ReleaseReadinessReport."""

from __future__ import annotations

import dataclasses
import json

from .models import ReleaseReadinessReport


def render_json(report: ReleaseReadinessReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
