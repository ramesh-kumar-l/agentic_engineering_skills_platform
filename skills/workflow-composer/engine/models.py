"""Shared data schema for Workflow Composer.

Every other engine module produces or consumes these types. A
`WorkflowTemplate` is a hardcoded, previously-dogfooded composition of
real skill CLIs (see `workflow_registry.py`) — this schema exists so the
registry, the compatibility checker, the step runner, and the renderers
all agree on one contract without importing each other directly.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class WiringMode(str, Enum):
    """How a step's input is built from the previous step's output.

    CLI_FLAG: the previous step's output file path is passed as the value
    of a named flag on this step's CLI invocation (e.g. `--ci-report`).

    TEXT_APPEND: the previous step's output has no matching CLI flag on
    this step (confirmed against the real, shipped CLI — see
    `acceptance-test-engineer/engine/cli.py`, which accepts only free
    text). A short excerpt derived from the previous step's output is
    appended to this step's task/requirement text instead, reproducing
    how Phase 3's real Pilot B actually composed these two skills.
    """

    CLI_FLAG = "cli_flag"
    TEXT_APPEND = "text_append"


class StepStatus(str, Enum):
    PENDING = "PENDING"
    OK = "OK"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class WorkflowStep:
    skill_name: str  # directory name under skills/, e.g. "feature-planner"
    output_filename: str  # e.g. "report.json" — the file this step writes
    wiring_mode: WiringMode
    wiring_flag: str | None = None  # required when wiring_mode is CLI_FLAG
    upstream_context_marker: str | None = None
    # ^ text expected to appear in this step's own SKILL.md "Required
    # Context"/"Preconditions" section, naming the upstream skill — used
    # by compatibility_checker.py to detect drift. None for step 1 (no
    # upstream in the chain).


@dataclass
class WorkflowTemplate:
    name: str
    description: str
    steps: list[WorkflowStep]


@dataclass
class CompatibilityIssue:
    step_skill_name: str
    detail: str


@dataclass
class StepResult:
    step: WorkflowStep
    status: StepStatus
    exit_code: int | None = None
    output_path: str | None = None
    duration_seconds: float | None = None
    stderr_excerpt: str | None = None


@dataclass
class WorkflowRunReport:
    template_name: str
    repo_path: str
    task_description: str
    dry_run: bool
    compatibility_issues: list[CompatibilityIssue] = field(default_factory=list)
    step_results: list[StepResult] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
