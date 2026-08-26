"""Sequences a WorkflowTemplate's steps and produces a WorkflowRunReport.

Fails CLOSED (ADR-020) — deliberately the opposite default from
context-optimizer's ADR-019 content-inclusion inversion, because building
on top of a broken or drifted step is the expensive failure here, not the
cheap one:

- A compatibility-check issue blocks all real execution outright — no
  step runs on a declared wiring that no longer matches the target
  skill's real contract.
- Any step's FAILED result stops the chain immediately; every remaining
  step is recorded SKIPPED, never run against stale/absent upstream data.
"""

from __future__ import annotations

from pathlib import Path

from .compatibility_checker import check_template
from .models import StepResult, StepStatus, WorkflowRunReport, WorkflowTemplate
from .skill_locator import resolve_skill_dir
from .step_runner import prepare_downstream_input, run_step


def run_workflow(
    template: WorkflowTemplate,
    *,
    repo_path: Path,
    task_description: str,
    out_dir: Path,
    dry_run: bool = False,
    platform_root: Path | None = None,
) -> WorkflowRunReport:
    skills_root = (
        platform_root / "skills" if platform_root is not None
        else resolve_skill_dir(template.steps[0].skill_name).parent
    )
    report = WorkflowRunReport(
        template_name=template.name,
        repo_path=str(repo_path),
        task_description=task_description,
        dry_run=dry_run,
    )
    report.compatibility_issues = check_template(template, skills_root)

    if report.compatibility_issues and not dry_run:
        report.warnings.append(
            "compatibility check found drift — refusing to execute any step "
            "(ADR-020 fail-closed default); see compatibility_issues"
        )
        for step in template.steps:
            report.step_results.append(
                StepResult(step=step, status=StepStatus.SKIPPED)
            )
        return report

    chain_broken = False
    upstream_output_path: Path | None = None

    for index, step in enumerate(template.steps):
        step_out_dir = out_dir / f"step{index + 1}-{step.skill_name}"

        if chain_broken:
            report.step_results.append(
                StepResult(step=step, status=StepStatus.SKIPPED)
            )
            continue

        skill_dir = resolve_skill_dir(step.skill_name, platform_root)

        if index == 0:
            positional_arg = str(repo_path)
        else:
            task_file = prepare_downstream_input(
                step, task_description, upstream_output_path, step_out_dir
            )
            positional_arg = str(task_file)

        result = run_step(
            step,
            skill_dir=skill_dir,
            positional_arg=positional_arg,
            upstream_output_path=upstream_output_path,
            step_out_dir=step_out_dir,
            dry_run=dry_run,
        )
        report.step_results.append(result)

        if result.status == StepStatus.FAILED:
            chain_broken = True
        elif result.status == StepStatus.OK and result.output_path:
            upstream_output_path = Path(result.output_path)

    return report
