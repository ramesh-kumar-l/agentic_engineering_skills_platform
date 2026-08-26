"""Evaluation harness for the workflow-composer skill.

Two layers scored separately, per project-memory-bank/05-evaluation-framework.md:

1. Deterministic layer: for each fixture, either a real registry template
   is run (against the bundled `tiny-repo` fixture, real
   `codebase-intelligence`/downstream-skill subprocesses, exercising
   ADR-010's tenth reuse for real) or a small locally-built fake template
   is run against the pytest suite's own `fake-skills` fixtures (to
   deterministically exercise the fail-closed paths — a real skill failing
   or drifting on demand isn't reproducible). Every fixture's expected
   step-status sequence and compatibility-issue count is scored
   automatically.
2. Judgment layer: this skill's core value is the agent's own Workflow
   Composition Checklist walk, which code cannot generate (does this task
   actually fit a registered template, is a compatibility/chain-failure
   result trustworthy). `actual/*.actual.json` holds real cases this
   session's agent produced by actually reasoning about each fixture, not
   fabricated to match ground truth.

This is single-run, single-rater evidence (this session's agent only) —
NOT the inter-rater-agreement experiment project-memory-bank/16-
assumptions-and-validation.md (A5) calls for. This is the THIRTEENTH
judgment-based skill evaluated this way — see RESULTS.md's summary.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HARNESS_DIR = Path(__file__).resolve().parent
SKILL_ROOT = HARNESS_DIR.parents[1] / "skills" / "workflow-composer"
sys.path.insert(0, str(SKILL_ROOT))

from engine.cli import main as cli_main  # noqa: E402
from engine.executor import run_workflow  # noqa: E402
from engine.models import WiringMode, WorkflowStep, WorkflowTemplate  # noqa: E402
from engine.workflow_registry import get_template  # noqa: E402

TINY_REPO = SKILL_ROOT / "tests" / "fixtures" / "tiny-repo"
FAKE_SKILLS_ROOT = SKILL_ROOT / "tests" / "fixtures" / "fake-skills"


def _run_registry_case(expected: dict, out_dir: Path) -> dict:
    template = get_template(expected["template"])
    report = run_workflow(
        template, repo_path=TINY_REPO, task_description="dry-run plan validation only",
        out_dir=out_dir, dry_run=expected["dry_run"],
    )
    return {
        "step_statuses": [r.status.value for r in report.step_results],
        "compatibility_issue_count": len(report.compatibility_issues),
        "no_output_files": not any(out_dir.rglob("*.json")) if out_dir.exists() else True,
    }


def _run_fake_failure_case(expected: dict, out_dir: Path) -> dict:
    template = WorkflowTemplate(
        name="fake-3-step", description="d",
        steps=[
            WorkflowStep(skill_name="skill-a", output_filename="report.json",
                         wiring_mode=WiringMode.CLI_FLAG),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report"),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report"),
        ],
    )
    report = run_workflow(
        template, repo_path=TINY_REPO, task_description="TRIGGER_FAIL",
        out_dir=out_dir, dry_run=False, platform_root=FAKE_SKILLS_ROOT,
    )
    return {
        "step_statuses": [r.status.value for r in report.step_results],
        "compatibility_issue_count": len(report.compatibility_issues),
    }


def _run_fake_drift_case(expected: dict, out_dir: Path) -> dict:
    template = WorkflowTemplate(
        name="fake-drift", description="d",
        steps=[
            WorkflowStep(skill_name="skill-a", output_filename="report.json",
                         wiring_mode=WiringMode.CLI_FLAG),
            WorkflowStep(skill_name="skill-b", output_filename="out.json",
                         wiring_mode=WiringMode.CLI_FLAG, wiring_flag="--ci-report",
                         upstream_context_marker="skill-a"),
        ],
    )
    report = run_workflow(
        template, repo_path=TINY_REPO, task_description="anything",
        out_dir=out_dir, dry_run=False, platform_root=FAKE_SKILLS_ROOT,
    )
    return {
        "step_statuses": [r.status.value for r in report.step_results],
        "compatibility_issue_count": len(report.compatibility_issues),
    }


def _run_cli_unknown_template_case(expected: dict, out_dir: Path) -> dict:
    exit_code = cli_main(["not-a-real-template", "--repo-path", str(TINY_REPO),
                           "--dry-run", "--out-dir", str(out_dir)])
    return {"cli_exit_code": exit_code}


_RUNNERS = {
    "registry": _run_registry_case,
    "fake_failure": _run_fake_failure_case,
    "fake_drift": _run_fake_drift_case,
    "cli_unknown_template": _run_cli_unknown_template_case,
}


def score_deterministic_layer(actual: dict, expected: dict) -> tuple[int, list[str]]:
    mismatches: list[str] = []
    for key in ("step_statuses", "compatibility_issue_count", "no_output_files", "cli_exit_code"):
        if key not in expected:
            continue
        if actual.get(key) != expected[key]:
            mismatches.append(f"{key}: expected {expected[key]}, got {actual.get(key)}")
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
    runs_dir = HARNESS_DIR / "_run"

    results_lines = ["# Workflow Composer — Evaluation Results", ""]
    results_lines.append(
        "Deterministic layer (step statuses, compatibility-issue count, "
        "dry-run side-effect absence, CLI exit code) is scored "
        "automatically — real registry templates run against the bundled "
        "`tiny-repo` fixture, real subprocess execution; fail-closed paths "
        "(step failure, compatibility drift) run against the pytest "
        "suite's `fake-skills` fixtures for determinism. Judgment-layer "
        "Precision/Recall are computed against `actual/*.actual.json` — "
        "real Workflow Composition Checklist cases this session's agent "
        "produced by actually reasoning about each fixture, not fabricated "
        "to match ground truth. Safety and Explainability require "
        "independent human review and are NOT scored here."
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

        out_dir = runs_dir / name
        runner = _RUNNERS[expected["engine_mode"]]

        start = time.perf_counter()
        actual = runner(expected, out_dir)
        elapsed_ms = (time.perf_counter() - start) * 1000

        correctness, mismatches = score_deterministic_layer(actual, expected)
        if mismatches:
            all_deterministic_correct = False
        efficiency = 5 if elapsed_ms < 5000 else 3 if elapsed_ms < 15000 else 1

        results_lines.append(f"## {name}")
        results_lines.append("### Deterministic layer (step statuses + compatibility)")
        results_lines.append(f"- Correctness: {correctness}/5")
        results_lines.append(f"- Efficiency: {efficiency}/5 ({elapsed_ms:.2f}ms)")
        results_lines.append(f"- Mismatches: {mismatches if mismatches else 'none'}")
        results_lines.append(f"- Actual: {actual}")

        if actual_path.exists():
            actual_derivation = json.loads(actual_path.read_text(encoding="utf-8"))
            actual_cases = actual_derivation.get("cases", [])
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
        "This is the THIRTEENTH judgment-based skill evaluated this way (after"
        " adversarial-diff-reviewer, acceptance-test-engineer, feature-planner,"
        " security-context-guard, root-cause-analyzer, architecture-decision,"
        " refactoring-safety, regression-hunter, release-readiness,"
        " dependency-supply-chain, engineering-knowledge-capture, and"
        " context-optimizer) — see project-memory-bank/16-assumptions-and-"
        "validation.md (A5) and L8 in project-memory-bank/12-known-"
        "limitations.md. Same single-run, single-rater caveat: this session's"
        " agent authored the fixtures, the expected categories, AND the actual"
        " derivation. Treat these scores as evidence the workflow-composer"
        " engine is executable and internally consistent — including the"
        " tenth ADR-010 composition (cases 01/03), the TEXT_APPEND wiring mode"
        " (case 02), the fail-closed step-failure default (case 05), and the"
        " compatibility-drift pre-execution gate (case 06) — not as proof of"
        " real-world workflow-composition quality, and NOT as Experiment B"
        " (ADR-009) — real timing data in these results is disclosed evidence,"
        " never cited as validating A10's status."
    )

    (HARNESS_DIR / "RESULTS.md").write_text("\n".join(results_lines), encoding="utf-8")
    print(f"wrote {HARNESS_DIR / 'RESULTS.md'}")
    if not all_deterministic_correct:
        sys.exit(1)


if __name__ == "__main__":
    run()
