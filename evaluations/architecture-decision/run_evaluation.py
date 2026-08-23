"""Evaluation harness for the architecture-decision skill.

Two layers scored separately, per project-memory-bank/05-evaluation-framework.md:

1. Deterministic layer: decision-quality anti-pattern flags AND per-option
   blast-radius scoring (keyword relevance + fan-in/fan-out/hotspot rollup,
   ADR-013) — scored automatically, actual engine output diffed against
   hand-authored ground truth. Each fixture pairs a decision.txt with a
   synthetic ci_report.json (matching codebase-intelligence's real
   report.json schema) so the required-composition precondition (reusing
   project-memory-bank/11-decisions.md ADR-010's pattern a third time) is
   exercised on every fixture, not bypassed.
2. Judgment layer: this skill's core value is the agent's own derivation of
   a decision record against the 10-category Architecture Decision Record
   checklist, which code cannot generate. `actual/*.actual.json` holds real
   cases this session's agent produced by actually following the SKILL.md
   workflow against each fixture (not fabricated to match the ground
   truth). This script scores those actual cases against expected
   categories via category match plus a keyword hit, computing
   Precision/Recall/False Positives/False Negatives.

This is single-run, single-rater evidence (this session's agent only) — NOT
the inter-rater-agreement experiment project-memory-bank/16-assumptions-and-
validation.md (A5) calls for. This is the SIXTH judgment-based skill
evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer,
feature-planner, security-context-guard, and root-cause-analyzer) — see
RESULTS.md's summary for that caveat.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
ENGINE_ROOT = HARNESS_DIR.parents[1] / "skills" / "architecture-decision"
sys.path.insert(0, str(ENGINE_ROOT))

from engine.report import build_report  # noqa: E402


def score_decision_flags(actual_ids: set[str], expected_ids: set[str]) -> tuple[int, list[str]]:
    mismatches: list[str] = []
    missing = expected_ids - actual_ids
    extra = actual_ids - expected_ids
    if missing:
        mismatches.append(f"missing decision flags: {sorted(missing)}")
    if extra:
        mismatches.append(f"unexpected decision flags: {sorted(extra)}")
    correctness = 5 if not mismatches else max(0, 5 - 2 * len(mismatches))
    return correctness, mismatches


def _case_text(case: dict) -> str:
    parts = [
        case.get("description", ""),
        case.get("grounding", ""),
        case.get("assumptions") or "",
    ]
    return " ".join(parts).lower()


def _case_matches(actual_case: dict, expected_case: dict) -> bool:
    if actual_case.get("category") != expected_case.get("category"):
        return False
    text = _case_text(actual_case)
    keywords = expected_case.get("keywords", [])
    return any(keyword.lower() in text for keyword in keywords)


def score_judgment_layer(actual_cases: list[dict], expected_cases: list[dict]) -> dict:
    matched_actual_ids: set[str] = set()
    true_positives = 0
    for expected_case in expected_cases:
        hit = next(
            (a for a in actual_cases if a["id"] not in matched_actual_ids and _case_matches(a, expected_case)),
            None,
        )
        if hit:
            matched_actual_ids.add(hit["id"])
            true_positives += 1

    false_negatives = len(expected_cases) - true_positives
    false_positives = len(actual_cases) - len(matched_actual_ids)

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

    results_lines = ["# Architecture Decision — Evaluation Results", ""]
    results_lines.append(
        "Deterministic layer (decision-quality anti-pattern flags + codebase-"
        "intelligence-grounded, per-option blast-radius scoring) is scored "
        "automatically. Judgment-layer Precision/Recall are computed against "
        "`actual/*.actual.json` — real decision-record cases this session's "
        "agent produced by actually performing the derivation, not fabricated "
        "to match ground truth. Safety and Explainability require independent "
        "human review and are NOT scored here "
        "(project-memory-bank/05-evaluation-framework.md)."
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

        decision_text = (fixture_dir / "decision.txt").read_text(encoding="utf-8")
        ci_report_path = fixture_dir / "ci_report.json"
        start = time.perf_counter()
        report = build_report(decision_text, str(ci_report_path))
        elapsed_ms = (time.perf_counter() - start) * 1000

        actual_ids = {f.pattern_id for f in report.flags}
        expected_ids = set(expected.get("decision_flag_ids", []))
        correctness, mismatches = score_decision_flags(actual_ids, expected_ids)
        if mismatches:
            all_deterministic_correct = False
        efficiency = 5 if elapsed_ms < 100 else 3 if elapsed_ms < 500 else 1

        results_lines.append(f"## {name}")
        results_lines.append("### Deterministic layer (decision flags + option impacts)")
        results_lines.append(f"- Correctness: {correctness}/5")
        results_lines.append(f"- Efficiency: {efficiency}/5 ({elapsed_ms:.2f}ms)")
        results_lines.append(f"- Mismatches: {mismatches if mismatches else 'none'}")
        results_lines.append(
            "- Option impacts: "
            f"{[(oi.option_label, oi.blast_radius_tier, oi.blast_radius_score) for oi in report.option_impacts]}"
        )

        if actual_path.exists():
            actual = json.loads(actual_path.read_text(encoding="utf-8"))
            actual_cases = actual.get("cases", [])
            expected_cases = expected.get("expected_categories", [])
            scores = score_judgment_layer(actual_cases, expected_cases)
            if scores["precision"] < 1.0 or scores["recall"] < 1.0:
                all_judgment_perfect = False
            results_lines.append("### Judgment layer (this session's actual derivation)")
            results_lines.append(f"- Precision: {scores['precision']}")
            results_lines.append(f"- Recall: {scores['recall']}")
            results_lines.append(f"- True Positives: {scores['true_positives']}")
            results_lines.append(f"- False Positives: {scores['false_positives']}")
            results_lines.append(f"- False Negatives: {scores['false_negatives']}")
        else:
            results_lines.append("### Judgment layer")
            results_lines.append("- No actual.json found — not yet derived.")
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
        "This is the SIXTH judgment-based skill evaluated this way (after"
        " adversarial-diff-reviewer, acceptance-test-engineer, feature-planner,"
        " security-context-guard, and root-cause-analyzer) — see"
        " `project-memory-bank/16-assumptions-and-validation.md` (A5) and L8 in"
        " `project-memory-bank/12-known-limitations.md`. Same single-run,"
        " single-rater caveat: this session's agent authored the fixtures, the"
        " expected decision-record categories, AND the actual derivation. Treat"
        " these scores as evidence the workflow is executable and internally"
        " consistent on synthetic fixtures — including the required"
        " codebase-intelligence composition, which every fixture exercises for"
        " real — not as proof of real-world architecture-decision quality. The"
        " inter-rater-agreement experiment A5 calls for has still not been run."
        " Case-01 and case-05 also surfaced a real, disclosed limitation: the"
        " keyword scorer treats a shared path prefix (here, every module under"
        " `engine/`) as a relevance signal, inflating blast radius for options"
        " that never actually mention the extra modules — the same class of"
        " limitation already logged as L14 (feature-planner) and L19"
        " (root-cause-analyzer)."
    )

    (HARNESS_DIR / "RESULTS.md").write_text("\n".join(results_lines), encoding="utf-8")
    print(f"wrote {HARNESS_DIR / 'RESULTS.md'}")
    if not all_deterministic_correct:
        sys.exit(1)


if __name__ == "__main__":
    run()
