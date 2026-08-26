"""Fake step-1 skill used only by workflow-composer's own unit tests.

Mimics codebase-intelligence's shape: positional repo path, --format,
--out. Always succeeds, writing a minimal report.json.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--format", default="json")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "report.json").write_text(
        json.dumps({"file_count": 1, "dependency_graph": {"hotspots": []}, "entry_points": []}),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
