"""Full-detail JSON rendering of a ContextOptimizationReport."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import ContextOptimizationReport


def render_json(report: ContextOptimizationReport, indent: int = 2) -> str:
    return json.dumps(asdict(report), indent=indent, sort_keys=False)
