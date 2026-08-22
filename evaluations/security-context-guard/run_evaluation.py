"""Evaluation harness for the security-context-guard skill.

Two layers scored separately, per project-memory-bank/05-evaluation-framework.md:

1. Deterministic layer: secret/PII/sensitive-path/action-category matches
   PLUS the sensitivity/suggested_verdict rollup — scored automatically,
   actual engine output diffed against hand-authored ground truth (same
   rigor as Phases 1-4). Each fixture pairs content.txt/action.txt/paths.json
   (one fixture also adds an optional ci_report.json, exercising the
   optional-composition path — unlike feature-planner's ADR-010 mandatory
   one).
2. Judgment layer: this skill's core value is the agent's own derivation
   against the 7-category Security Decision Checklist, which code cannot
   generate. `actual/*.actual.json` holds real cases this session's agent
   produced by actually following the SKILL.md workflow against each
   fixture (not fabricated to match the ground truth). This script scores
   those actual cases against expected checklist categories via category
   match plus a keyword hit, computing Precision/Recall/False
   Positives/False Negatives.

This is single-run, single-rater evidence (this session's agent only) — NOT
the inter-rater-agreement experiment project-memory-bank/16-assumptions-and-
validation.md (A5) calls for. This is the FOURTH judgment-based skill
evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer,
and feature-planner) — see RESULTS.md's summary for that caveat.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
ENGINE_ROOT = HARNESS_DIR.parents[1] / "skills" / "security-context-guard"
sys.path.insert(0, str(ENGINE_ROOT))

from engine.report import build_report  # noqa: E402


def score_deterministic(report, expected: dict) -> tuple[int, list[str]]:
    mismatches: list[str] = []

    actual_field_pairs = [
        ("secret_pattern_ids", {m.pattern_id for m in report.secrets}),
        ("pii_pattern_ids", {m.pattern_id for m in report.pii}),
        ("sensitive_path_pattern_ids", {m.pattern_id for m in report.sensitive_paths}),
        ("action_pattern_ids", {m.pattern_id for m in report.action_flags}),
    ]
    for field_name, actual_ids in actual_field_pairs:
        expected_ids = set(expected.get(field_name, []))
        missing = expected_ids - actual_ids
        extra = actual_ids - expected_ids
        if missing:
            mismatches.append(f"missing {field_name}: {sorted(missing)}")
        if extra:
            mismatches.append(f"unexpected {field_name}: {sorted(extra)}")

    if report.classification.sensitivity != expected.get("expected_sensitivity"):
        mismatches.append(
            f"sensitivity mismatch: got {report.classification.sensitivity!r}, "
            f"expected {expected.get('expected_sensitivity')!r}"
        )
    if report.classification.suggested_verdict != expected.get("expected_suggested_verdict"):
        mismatches.append(
            f"suggested_verdict mismatch: got {report.classification.suggested_verdict!r}, "
            f"expected {expected.get('expected_suggested_verdict')!r}"
        )

    correctness = 5 if not mismatches else max(0, 5 - len(mismatches))
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

    results_lines = ["# Security Context Guard — Evaluation Results", ""]
    results_lines.append(
        "Deterministic layer (secret/PII/sensitive-path/action-category matching"
        " plus the sensitivity/suggested_verdict rollup) is scored automatically."
        " Judgment-layer Precision/Recall are computed against `actual/*.actual.json`"
        " — real Security Decision Checklist cases this session's agent produced by"
        " actually performing the derivation, not fabricated to match ground truth."
        " Safety and Explainability require independent human review and are NOT"
        " scored here (project-memory-bank/05-evaluation-framework.md)."
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

        content_text = (fixture_dir / "content.txt").read_text(encoding="utf-8")
        action_text = (fixture_dir / "action.txt").read_text(encoding="utf-8")
        paths = json.loads((fixture_dir / "paths.json").read_text(encoding="utf-8"))
        ci_report_file = fixture_dir / "ci_report.json"
        ci_report_path = str(ci_report_file) if ci_report_file.exists() else None

        start = time.perf_counter()
        report = build_report(content_text, action_text, paths, ci_report_path)
        elapsed_ms = (time.perf_counter() - start) * 1000

        correctness, mismatches = score_deterministic(report, expected)
        if mismatches:
            all_deterministic_correct = False
        efficiency = 5 if elapsed_ms < 100 else 3 if elapsed_ms < 500 else 1

        results_lines.append(f"## {name}")
        results_lines.append("### Deterministic layer (classification + matches)")
        results_lines.append(f"- Correctness: {correctness}/5")
        results_lines.append(f"- Efficiency: {efficiency}/5 ({elapsed_ms:.2f}ms)")
        results_lines.append(f"- Mismatches: {mismatches if mismatches else 'none'}")
        results_lines.append(
            f"- sensitivity={report.classification.sensitivity}, "
            f"suggested_verdict={report.classification.suggested_verdict}, "
            f"uncertain={report.classification.uncertain}"
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
        "This is the FOURTH judgment-based skill evaluated this way (after"
        " adversarial-diff-reviewer, acceptance-test-engineer, and"
        " feature-planner) — see `project-memory-bank/16-assumptions-and-"
        "validation.md` (A5) and L8 in `project-memory-bank/12-known-"
        "limitations.md`. Same single-run, single-rater caveat: this session's"
        " agent authored the fixtures, the expected checklist categories, AND"
        " the actual derivation. Treat these scores as evidence the workflow is"
        " executable and internally consistent on synthetic fixtures — including"
        " the fail-closed-under-uncertainty default (case-08) — not as proof of"
        " real-world security-judgment quality. The inter-rater-agreement"
        " experiment A5 calls for has still not been run."
    )

    (HARNESS_DIR / "RESULTS.md").write_text("\n".join(results_lines), encoding="utf-8")
    print(f"wrote {HARNESS_DIR / 'RESULTS.md'}")
    if not all_deterministic_correct:
        sys.exit(1)


if __name__ == "__main__":
    run()
