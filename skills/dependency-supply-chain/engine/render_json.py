"""Renders a DependencySupplyChainReport as canonical JSON."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import DependencySupplyChainReport


def render_json(report: DependencySupplyChainReport) -> str:
    return json.dumps(asdict(report), indent=2, sort_keys=False)
