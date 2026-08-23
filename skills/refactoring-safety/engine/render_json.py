"""Full-detail JSON rendering of a RefactoringSafetyReport."""

from __future__ import annotations

import dataclasses
import json

from .models import RefactoringSafetyReport


def render_json(report: RefactoringSafetyReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
