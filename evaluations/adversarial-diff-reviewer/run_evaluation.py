"""Evaluation harness for the adversarial-diff-reviewer skill.

Two layers scored separately, per project-memory-bank/05-evaluation-framework.md:

1. Deterministic risk-flag layer: scored automatically, same as Phase 1 —
   actual engine output diffed against hand-authored ground truth.
2. Judgment layer: this skill's core value is the agent's own adversarial
   reasoning, which code cannot generate. `actual/*.actual.json` holds real
   findings this session's agent produced by actually following the SKILL.md
   workflow against each fixture (not fabricated to match the ground truth).
   This script scores those actual findings against expected defects via
   category+file match plus a keyword hit in the description, computing
   Precision/Recall/False Positives/False Negatives.

This is single-run, single-rater evidence (this session's agent only) — NOT
the inter-rater-agreement experiment project-memory-bank/16-assumptions-and-
validation.md (A5) calls for. See RESULTS.md's summary for that caveat.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
ENGINE_ROOT = HARNESS_DIR.parents[1] / "skills" / "adversarial-diff-reviewer"
sys.path.insert(0, str(ENGINE_ROOT))

from engine.report import build_report  # noqa: E402


def score_risk_flags(actual_pattern_ids: set[str], expected_pattern_ids: set[str]) -> tuple[int, list[str]]:
    mismatches: list[str] = []
    missing = expected_pattern_ids - actual_pattern_ids
    extra = actual_pattern_ids - expected_pattern_ids
    if missing:
        mismatches.append(f"missing risk flags: {sorted(missing)}")
    if extra:
        mismatches.append(f"unexpected risk flags: {sorted(extra)}")
    correctness = 5 if not mismatches else max(0, 5 - 2 * len(mismatches))
    return correctness, mismatches


def _defect_matches(actual_defect: dict, expected_defect: dict) -> bool:
    if actual_defect.get("category") != expected_defect.get("category"):
        return False
    if actual_defect.get("file") != expected_defect.get("file"):
        return False
    description = actual_defect.get("description", "").lower()
    keywords = expected_defect.get("keywords", [])
    return any(keyword.lower() in description for keyword in keywords)


def score_judgment_layer(actual_defects: list[dict], expected_defects: list[dict]) -> dict:
    matched_actual_ids: set[str] = set()
    true_positives = 0
    for expected_defect in expected_defects:
        hit = next(
            (a for a in actual_defects if a["id"] not in matched_actual_ids and _defect_matches(a, expected_defect)),
            None,
        )
        if hit:
            matched_actual_ids.add(hit["id"])
            true_positives += 1

    false_negatives = len(expected_defects) - true_positives
    false_positives = len(actual_defects) - len(matched_actual_ids)

    precision = (
        true_positives / (true_positives + false_positives)
        if (true_positives + false_positives) > 0
        else 1.0
    )
    recall = (
        true_positives / (true_positives + false_negatives)
        if (true_positives + false_negatives) > 0
        else 1.0
    )
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives,
        "precision": round(precision, 2),
        "recall": round(recall, 2),
    }


def run() -> None:
    fixtures_dir = HARNESS_DIR / "fixtures"
    expected_dir = HARNESS_DIR / "expected"
    actual_dir = HARNESS_DIR / "actual"

    results_lines = ["# Adversarial Diff Reviewer — Evaluation Results", ""]
    results_lines.append(
        "Deterministic risk-flag layer is scored automatically. Judgment-layer"
        " Precision/Recall are computed against `actual/*.actual.json` — real"
        " findings this session's agent produced by actually performing the"
        " adversarial review, not fabricated to match ground truth. Safety and"
        " Explainability require independent human review and are NOT scored"
        " here (project-memory-bank/05-evaluation-framework.md)."
    )
    results_lines.append("")

    all_deterministic_correct = True
    all_judgment_perfect = True

    for fixture_dir in sorted(fixtures_dir.iterdir()):
        if not fixture_dir.is_dir():
            continue
        name = fixture_dir.name
        expected_path = expected_dir / f"{name}.expected.json"
        actual_path = actual_dir / f"{name}.actual.json"
        if not expected_path.exists():
            continue
        expected = json.loads(expected_path.read_text(encoding="utf-8"))

        diff_text = (fixture_dir / "change.diff").read_text(encoding="utf-8")
        start = time.perf_counter()
        report = build_report(diff_text)
        elapsed_ms = (time.perf_counter() - start) * 1000

        actual_pattern_ids = {f.pattern_id for f in report.risk_flags}
        expected_pattern_ids = set(expected.get("risk_flag_pattern_ids", []))
        correctness, mismatches = score_risk_flags(actual_pattern_ids, expected_pattern_ids)
        if mismatches:
            all_deterministic_correct = False
        efficiency = 5 if elapsed_ms < 100 else 3 if elapsed_ms < 500 else 1

        results_lines.append(f"## {name}")
        results_lines.append("### Deterministic risk-flag layer")
        results_lines.append(f"- Correctness: {correctness}/5")
        results_lines.append(f"- Efficiency: {efficiency}/5 ({elapsed_ms:.2f}ms)")
        results_lines.append(f"- Mismatches: {mismatches if mismatches else 'none'}")

        if actual_path.exists():
            actual = json.loads(actual_path.read_text(encoding="utf-8"))
            actual_defects = actual.get("defects", [])
            expected_defects = expected.get("defects", [])
            scores = score_judgment_layer(actual_defects, expected_defects)
            if scores["precision"] < 1.0 or scores["recall"] < 1.0:
                all_judgment_perfect = False
            results_lines.append("### Judgment layer (this session's actual review)")
            results_lines.append(f"- Precision: {scores['precision']}")
            results_lines.append(f"- Recall: {scores['recall']}")
            results_lines.append(f"- True Positives: {scores['true_positives']}")
            results_lines.append(f"- False Positives: {scores['false_positives']}")
            results_lines.append(f"- False Negatives: {scores['false_negatives']}")
        else:
            results_lines.append("### Judgment layer")
            results_lines.append("- No actual.json found — not yet reviewed.")
        results_lines.append("- Safety: _human review required_")
        results_lines.append("- Explainability: _human review required_")
        results_lines.append("")

    results_lines.append("## Summary")
    results_lines.append(
        "Deterministic layer: "
        + ("all cases correct." if all_deterministic_correct else "one or more mismatches — see above.")
    )
    results_lines.append(
        "Judgment layer: "
        + (
            "perfect precision/recall across all 8 fixtures."
            if all_judgment_perfect
            else "one or more fixtures had imperfect precision/recall — see above."
        )
    )
    results_lines.append("")
    results_lines.append(
        "This is the first evidence for a judgment-based skill in"
        " `project-memory-bank/16-assumptions-and-validation.md` (A5). It is"
        " single-run, single-rater evidence from this session's agent — the"
        " inter-rater-agreement experiment A5 calls for has NOT been run (that"
        " requires a second, independent reviewer/session). Treat these scores"
        " as evidence the workflow is executable and internally consistent on"
        " synthetic fixtures, not as proof of real-world review quality."
    )

    (HARNESS_DIR / "RESULTS.md").write_text("\n".join(results_lines), encoding="utf-8")
    print(f"wrote {HARNESS_DIR / 'RESULTS.md'}")
    if not all_deterministic_correct:
        sys.exit(1)


if __name__ == "__main__":
    run()
