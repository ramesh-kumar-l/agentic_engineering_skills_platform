"""Fake step-2 skill used only by workflow-composer's own unit tests.

Mimics a downstream skill: positional task file, optional --ci-report
flag, --format, --out. Exits non-zero without writing output when the
task file's content contains TRIGGER_FAIL, so executor tests can exercise
fail-closed sequencing deterministically.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    parser.add_argument("--ci-report", default=None)
    parser.add_argument("--format", default="json")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    task_text = Path(args.path).read_text(encoding="utf-8")
    if "TRIGGER_FAIL" in task_text:
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "out.json").write_text(
        json.dumps({"received_ci_report": args.ci_report, "task_text": task_text}),
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
