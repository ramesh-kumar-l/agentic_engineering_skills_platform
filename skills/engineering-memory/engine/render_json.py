"""Renders a MemoryQueryReport as canonical JSON."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import MemoryQueryReport


def render_json(report: MemoryQueryReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=False)
