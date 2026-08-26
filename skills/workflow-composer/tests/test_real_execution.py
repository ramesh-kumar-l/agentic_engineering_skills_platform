"""The one test in this suite that actually subprocess-invokes other
skills' real CLIs — no prior skill's test suite in this portfolio does
this, so it's a genuinely new kind of coverage, not folded silently into
the unit tests above. Runs `understand-then-plan` for real against the
tiny synthetic fixture repo bundled alongside this file."""

import json
from pathlib import Path

from engine.executor import run_workflow
from engine.models import StepStatus
from engine.workflow_registry import get_template

_TINY_REPO = Path(__file__).parent / "fixtures" / "tiny-repo"


def test_understand_then_plan_runs_for_real(tmp_path):
    template = get_template("understand-then-plan")
    report = run_workflow(
        template,
        repo_path=_TINY_REPO,
        task_description="Add a subtract(a, b) function alongside add() in main.py.",
        out_dir=tmp_path / "out",
        dry_run=False,
    )

    assert report.compatibility_issues == []
    assert [r.status for r in report.step_results] == [StepStatus.OK, StepStatus.OK]

    ci_output = Path(report.step_results[0].output_path)
    plan_output = Path(report.step_results[1].output_path)
    assert ci_output.exists()
    assert plan_output.exists()

    ci_data = json.loads(ci_output.read_text(encoding="utf-8"))
    assert ci_data["file_count"] >= 2

    plan_data = json.loads(plan_output.read_text(encoding="utf-8"))
    assert plan_data  # feature-planner produced a real, non-empty report
