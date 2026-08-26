"""Evaluation harness for the dependency-supply-chain skill.

Two layers scored separately, per project-memory-bank/05-evaluation-framework.md:

1. Deterministic layer: the flag set (pattern_ids) and the report-level
   `suggested_risk_level` — scored automatically, actual engine output
   diffed against hand-authored ground truth. Each fixture supplies a
   synthetic ci_report.json (matching codebase-intelligence's real
   report.json schema, exercising the required-composition precondition —
   ADR-010, reused a seventh time — on every fixture).
2. Judgment layer: this skill's core value is the agent's own derivation of
   a dependency-risk assessment against the 8-category Dependency Risk
   Checklist, which code cannot generate. `actual/*.actual.json` holds real
   cases this session's agent produced by actually following the SKILL.md
   workflow against each fixture (not fabricated to match the ground
   truth). This script scores those actual cases against expected
   categories via category match plus a keyword hit, computing
   Precision/Recall/False Positives/False Negatives.

This is single-run, single-rater evidence (this session's agent only) — NOT
the inter-rater-agreement experiment project-memory-bank/16-assumptions-and-
validation.md (A5) calls for. This is the TENTH judgment-based skill
evaluated this way (after adversarial-diff-reviewer, acceptance-test-engineer,
feature-planner, security-context-guard, root-cause-analyzer,
architecture-decision, refactoring-safety, regression-hunter, and
release-readiness) — see RESULTS.md's summary for that caveat.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
ENGINE_ROOT = HARNESS_DIR.parents[1] / "skills" / "dependency-supply-chain"
sys.path.insert(0, str(ENGINE_ROOT))

from engine.report import build_report  # noqa: E402


def score_deterministic_layer(report, expected: dict) -> tuple[int, list[str]]:
    mismatches: list[str] = []

    actual_flag_ids = {f.pattern_id for f in report.flags}
    expected_flag_ids = set(expected.get("flag_ids", []))
    missing_flags = expected_flag_ids - actual_flag_ids
    extra_flags = actual_flag_ids - expected_flag_ids
    if missing_flags:
        mismatches.append(f"missing flags: {sorted(missing_flags)}")
    if extra_flags:
        mismatches.append(f"unexpected flags: {sorted(extra_flags)}")

    expected_level = expected.get("suggested_risk_level")
    if expected_level is not None and report.suggested_risk_level != expected_level:
        mismatches.append(
            f"suggested_risk_level: expected {expected_level}, got {report.suggested_risk_level}"
        )

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

    results_lines = ["# Dependency / Supply Chain — Evaluation Results", ""]
    results_lines.append(
        "Deterministic layer (flag set + suggested_risk_level) is scored "
        "automatically. Judgment-layer Precision/Recall are computed against "
        "`actual/*.actual.json` — real Dependency Risk Checklist cases this "
        "session's agent produced by actually performing the derivation, not "
        "fabricated to match ground truth. Safety and Explainability require "
        "independent human review and are NOT scored here "
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

        ci_report_path = fixture_dir / "ci_report.json"

        start = time.perf_counter()
        report = build_report(str(ci_report_path))
        elapsed_ms = (time.perf_counter() - start) * 1000

        correctness, mismatches = score_deterministic_layer(report, expected)
        if mismatches:
            all_deterministic_correct = False
        efficiency = 5 if elapsed_ms < 100 else 3 if elapsed_ms < 500 else 1

        results_lines.append(f"## {name}")
        results_lines.append("### Deterministic layer (flags + suggested_risk_level)")
        results_lines.append(f"- Correctness: {correctness}/5")
        results_lines.append(f"- Efficiency: {efficiency}/5 ({elapsed_ms:.2f}ms)")
        results_lines.append(f"- Mismatches: {mismatches if mismatches else 'none'}")
        results_lines.append(f"- suggested_risk_level: {report.suggested_risk_level}")
        results_lines.append(f"- Flags: {[f.pattern_id for f in report.flags]}")

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
        "This is the TENTH judgment-based skill evaluated this way (after"
        " adversarial-diff-reviewer, acceptance-test-engineer, feature-planner,"
        " security-context-guard, root-cause-analyzer, architecture-decision,"
        " refactoring-safety, regression-hunter, and release-readiness) — see"
        " `project-memory-bank/16-assumptions-and-validation.md` (A5) and"
        " L8 in `project-memory-bank/12-known-limitations.md`. Same single-run,"
        " single-rater caveat: this session's agent authored the fixtures, the"
        " expected checklist categories, AND the actual derivation. Treat these"
        " scores as evidence the workflow is executable and internally"
        " consistent on synthetic fixtures — including the required"
        " codebase-intelligence composition (every fixture) — not as proof of"
        " real-world dependency-risk judgment quality. The inter-rater-"
        " agreement experiment A5 calls for has still not been run. This skill"
        " also has no live CVE database and no per-dependency license data —"
        " see SKILL.md Known Limitations; the checklist's item 4 (license"
        " risk) is deliberately answered 'not available' in every case below,"
        " not fabricated."
    )

    (HARNESS_DIR / "RESULTS.md").write_text("\n".join(results_lines), encoding="utf-8")
    print(f"wrote {HARNESS_DIR / 'RESULTS.md'}")
    if not all_deterministic_correct:
        sys.exit(1)


if __name__ == "__main__":
    run()
