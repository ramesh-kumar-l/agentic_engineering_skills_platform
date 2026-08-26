"""Renders a KnowledgeCaptureReport as canonical JSON."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import KnowledgeCaptureReport


def render_json(report: KnowledgeCaptureReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=False)
