"""Writes and reads RunProvenance records as JSON files.

Layout: `evidence/runs/<skill_name>/<run_id>.json` — mirrors the existing
`evaluations/<skill>/` per-skill layout convention rather than inventing a
new one.
"""

from __future__ import annotations

import json
from pathlib import Path

from .schema import RunProvenance


def save(record: RunProvenance, runs_root: Path) -> Path:
    skill_dir = runs_root / record.skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    out_path = skill_dir / f"{record.run_id}.json"
    out_path.write_text(json.dumps(record.to_dict(), indent=2) + "\n", encoding="utf-8")
    return out_path


def load(path: Path) -> RunProvenance:
    data = json.loads(path.read_text(encoding="utf-8"))
    return RunProvenance.from_dict(data)
