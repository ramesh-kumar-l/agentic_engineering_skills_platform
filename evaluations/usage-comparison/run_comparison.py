"""Prints a per-task with_skill vs. plain_prompting summary from a filled-in
usage comparison run log.

Deterministic aggregation only — no judgment, no scoring, consistent with
this project's deterministic/judgment split (ADR-007). Reads real numbers
the user logged from their own agent client; fabricates nothing.

Usage:
    python run_comparison.py [path/to/run-log.csv]

Defaults to template-run-log.csv in this directory if no path is given.
Rows with blank turns_taken/approx_tokens/wall_clock_minutes (the shipped
template's placeholder rows) are skipped, not treated as zero.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from pathlib import Path

REQUIRED_ARMS = ("with_skill", "plain_prompting")


@dataclass
class Run:
    task_id: str
    arm: str
    turns_taken: float
    approx_tokens: float
    wall_clock_minutes: float
    outcome_correct: bool | None


def _parse_bool(value: str) -> bool | None:
    value = value.strip().lower()
    if value in ("true", "yes", "1"):
        return True
    if value in ("false", "no", "0"):
        return False
    return None


def load_runs(csv_path: Path) -> list[Run]:
    runs: list[Run] = []
    with csv_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            turns = row.get("turns_taken", "").strip()
            tokens = row.get("approx_tokens", "").strip()
            minutes = row.get("wall_clock_minutes", "").strip()
            if not (turns and tokens and minutes):
                continue  # unfilled template row — skip, don't treat as zero
            runs.append(
                Run(
                    task_id=row["task_id"].strip(),
                    arm=row["arm"].strip(),
                    turns_taken=float(turns),
                    approx_tokens=float(tokens),
                    wall_clock_minutes=float(minutes),
                    outcome_correct=_parse_bool(row.get("outcome_correct", "")),
                )
            )
    return runs


def summarize(runs: list[Run]) -> str:
    if not runs:
        return (
            "No filled-in rows found — this run log has no real data yet.\n"
            "Fill in template-run-log.csv with actual runs (see README.md) "
            "before expecting a summary."
        )

    by_task: dict[str, dict[str, Run]] = {}
    for run in runs:
        by_task.setdefault(run.task_id, {})[run.arm] = run

    lines = ["Task | Arm | Turns | ~Tokens | Minutes | Correct", "---|---|---|---|---|---"]
    for task_id in sorted(by_task):
        arms = by_task[task_id]
        for arm in REQUIRED_ARMS:
            run = arms.get(arm)
            if run is None:
                lines.append(f"{task_id} | {arm} | (no data logged) | | | ")
                continue
            correct = "yes" if run.outcome_correct else "no" if run.outcome_correct is False else "?"
            lines.append(
                f"{task_id} | {arm} | {run.turns_taken:g} | {run.approx_tokens:g} | "
                f"{run.wall_clock_minutes:g} | {correct}"
            )
        if "with_skill" in arms and "plain_prompting" in arms:
            skill_run = arms["with_skill"]
            plain_run = arms["plain_prompting"]
            token_delta = skill_run.approx_tokens - plain_run.approx_tokens
            time_delta = skill_run.wall_clock_minutes - plain_run.wall_clock_minutes
            lines.append(
                f"{task_id} | delta (skill - plain) | "
                f"{skill_run.turns_taken - plain_run.turns_taken:+g} | "
                f"{token_delta:+g} | {time_delta:+g} | "
            )

    lines.append("")
    lines.append(
        "Reminder: this is a self-run pilot (ADR-009 discipline), not a "
        "blinded experiment. A negative token/time delta here is a real "
        "data point worth taking seriously, not proof either way — see "
        "README.md."
    )
    return "\n".join(lines)


def main() -> int:
    default_path = Path(__file__).parent / "template-run-log.csv"
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    if not csv_path.exists():
        print(f"Run log not found: {csv_path}", file=sys.stderr)
        return 1
    runs = load_runs(csv_path)
    print(summarize(runs))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
