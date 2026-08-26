"""Evaluation harness for the engineering-memory skill.

Two layers scored separately, per project-memory-bank/05-evaluation-framework.md:

1. Deterministic layer: which record ids surface as matches, which are
   flagged stale, and (for the top-n / precondition-failure / corpus-
   drift cases) the match count / raised-error / warning behavior —
   scored automatically, actual engine output diffed against
   hand-authored ground truth. Each fixture supplies `task.txt`,
   `decisions.md`, `limitations.md`, and (except case-07, which omits it
   on purpose) `ci_report.json` — exercising the required-composition
   precondition (ADR-010, reused an eleventh time) on every fixture that
   has one.
2. Judgment layer: this skill's core value is the agent's own derivation
   of an Engineering Memory Retrieval Checklist walk, which code cannot
   generate. `actual/*.actual.json` holds real cases this session's agent
   produced by actually following the SKILL.md workflow against each
   fixture (not fabricated to match the ground truth). This script scores
   those actual cases against expected categories via category match plus
   a keyword hit, computing Precision/Recall/False Positives/False
   Negatives.

This is single-run, single-rater evidence (this session's agent only) —
NOT the inter-rater-agreement experiment project-memory-bank/16-
assumptions-and-validation.md (A5) calls for. This is the FOURTEENTH
judgment-based skill evaluated this way — see RESULTS.md's summary for
that caveat.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
ENGINE_ROOT = HARNESS_DIR.parents[1] / "skills" / "engineering-memory"
sys.path.insert(0, str(ENGINE_ROOT))

from engine.ci_report_loader import CiReportError  # noqa: E402
from engine.report import build_report  # noqa: E402


def score_deterministic_layer(report, error_raised, expected: dict) -> tuple[int, list[str]]:
    mismatches: list[str] = []

    expect_error = expected.get("expect_error", False)
    if expect_error:
        if not error_raised:
            mismatches.append("expected a CiReportError, none was raised")
        correctness = 5 if not mismatches else 0
        return correctness, mismatches
    if error_raised:
        mismatches.append(f"unexpected error raised: {error_raised}")
        return 0, mismatches

    actual_ids = {m.record.record_id for m in report.matches}
    expected_match_ids = set(expected.get("expected_match_ids", []))
    expected_absent_ids = set(expected.get("expected_absent_ids", []))
    missing = expected_match_ids - actual_ids
    unexpected_present = actual_ids & expected_absent_ids
    if missing:
        mismatches.append(f"missing expected matches: {sorted(missing)}")
    if unexpected_present:
        mismatches.append(f"matches that should have been excluded: {sorted(unexpected_present)}")

    expected_stale_ids = set(expected.get("expected_stale_ids", []))
    actual_stale_ids = {m.record.record_id for m in report.matches if m.staleness.is_stale}
    stale_mismatch = expected_stale_ids - actual_stale_ids
    if stale_mismatch:
        mismatches.append(f"expected stale but not flagged: {sorted(stale_mismatch)}")

    expected_rank_order = expected.get("expected_rank_order")
    if expected_rank_order:
        actual_order = [m.record.record_id for m in report.matches if m.record.record_id in expected_rank_order]
        filtered_expected = [rid for rid in expected_rank_order if rid in actual_order]
        if actual_order != filtered_expected:
            mismatches.append(f"expected rank order {filtered_expected}, got {actual_order}")

    expected_count = expected.get("expected_match_count")
    if expected_count is not None and len(report.matches) != expected_count:
        mismatches.append(f"expected {expected_count} matches, got {len(report.matches)}")

    expected_warning_substring = expected.get("expected_warning_substring")
    if expected_warning_substring is not None:
        if not any(expected_warning_substring in w.lower() for w in report.warnings):
            mismatches.append(f"expected a warning containing {expected_warning_substring!r}")

    correctness = 5 if not mismatches else max(0, 5 - 2 * len(mismatches))
    return correctness, mismatches


def _case_text(case: dict) -> str:
    parts = [case.get("description", ""), case.get("grounding", ""), case.get("assumptions") or ""]
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

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 1.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 1.0
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

    results_lines = ["# Engineering Memory — Evaluation Results", ""]
    results_lines.append(
        "Deterministic layer (which record ids match, which are flagged "
        "stale, match count / raised-error / warning behavior) is scored "
        "automatically. Judgment-layer Precision/Recall are computed "
        "against `actual/*.actual.json` — real Engineering Memory "
        "Retrieval Checklist cases this session's agent produced by "
        "actually performing the derivation, not fabricated to match "
        "ground truth. Safety and Explainability require independent "
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

        task_text = (fixture_dir / "task.txt").read_text(encoding="utf-8")
        ci_report_path = fixture_dir / "ci_report.json"
        decisions_path = fixture_dir / "decisions.md"
        limitations_path = fixture_dir / "limitations.md"
        top_n = expected.get("top_n", 10)

        report = None
        error_raised = None
        start = time.perf_counter()
        try:
            report = build_report(
                task_text, str(ci_report_path), str(decisions_path), str(limitations_path), top_n=top_n
            )
        except CiReportError as exc:
            error_raised = str(exc)
        elapsed_ms = (time.perf_counter() - start) * 1000

        correctness, mismatches = score_deterministic_layer(report, error_raised, expected)
        if mismatches:
            all_deterministic_correct = False
        efficiency = 5 if elapsed_ms < 100 else 3 if elapsed_ms < 500 else 1

        results_lines.append(f"## {name}")
        results_lines.append("### Deterministic layer (matches + staleness + count/error/warning)")
        results_lines.append(f"- Correctness: {correctness}/5")
        results_lines.append(f"- Efficiency: {efficiency}/5 ({elapsed_ms:.2f}ms)")
        results_lines.append(f"- Mismatches: {mismatches if mismatches else 'none'}")
        if error_raised is not None:
            results_lines.append(f"- Error raised: {error_raised}")
        elif report is not None:
            results_lines.append(
                f"- Matches: {[(m.record.record_id, m.score, m.staleness.is_stale) for m in report.matches]}"
            )
            if report.warnings:
                results_lines.append(f"- Warnings: {report.warnings}")

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
        "This is the FOURTEENTH judgment-based skill evaluated this way (after"
        " adversarial-diff-reviewer, acceptance-test-engineer, feature-planner,"
        " security-context-guard, root-cause-analyzer, architecture-decision,"
        " refactoring-safety, regression-hunter, release-readiness,"
        " dependency-supply-chain, engineering-knowledge-capture,"
        " context-optimizer, and workflow-composer) — see `project-memory-"
        "bank/16-assumptions-and-validation.md` (A5) and L8 in"
        " `project-memory-bank/12-known-limitations.md`. Same single-run,"
        " single-rater caveat: this session's agent authored the fixtures,"
        " the expected checklist categories, AND the actual derivation."
        " Treat these scores as evidence the retrieval pipeline is"
        " executable and internally consistent on synthetic fixtures —"
        " including the required codebase-intelligence composition (every"
        " fixture with a report), whole-token collision resistance"
        " (case-03), and both staleness paths (case-04's FIXED-title path,"
        " case-05's module-no-longer-exists path) — not as proof of"
        " real-world retrieval-relevance judgment quality, and NOT as"
        " evidence toward A8 (project-memory-bank/16-assumptions-and-"
        "validation.md), which this build only creates the capability for."
        " The inter-rater-agreement experiment A5 calls for has still not"
        " been run. This skill also never writes into the memory bank"
        " itself and this pass's corpus is limited to 11-decisions.md and"
        " 12-known-limitations.md — see SKILL.md Known Limitations."
    )

    (HARNESS_DIR / "RESULTS.md").write_text("\n".join(results_lines), encoding="utf-8")
    print(f"wrote {HARNESS_DIR / 'RESULTS.md'}")
    if not all_deterministic_correct:
        sys.exit(1)


if __name__ == "__main__":
    run()
