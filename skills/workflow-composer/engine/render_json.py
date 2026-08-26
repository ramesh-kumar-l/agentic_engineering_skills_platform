"""JSON rendering for a WorkflowRunReport."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import WorkflowRunReport
from .stats import compute_stats


def render_json(report: WorkflowRunReport) -> str:
    payload = asdict(report)
    payload["stats"] = compute_stats(report)
    return json.dumps(payload, indent=2, default=str)
