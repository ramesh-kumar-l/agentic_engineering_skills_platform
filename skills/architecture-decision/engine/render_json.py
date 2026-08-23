"""Full-detail JSON rendering of an ArchitectureDecisionReport."""

from __future__ import annotations

import dataclasses
import json

from .models import ArchitectureDecisionReport


def render_json(report: ArchitectureDecisionReport, indent: int = 2) -> str:
    return json.dumps(dataclasses.asdict(report), indent=indent)
