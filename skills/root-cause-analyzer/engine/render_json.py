"""Full-detail JSON rendering of a RootCauseReport."""

from __future__ import annotations

import dataclasses
import json

from .models import RootCauseReport


def render_json(report: RootCauseReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
