from engine.compatibility_checker import check_template
from engine.models import WiringMode, WorkflowStep, WorkflowTemplate

_GOOD_SKILL_MD = """# Fake Skill

## Preconditions
- A codebase-intelligence report.json already generated.

## Required Context
Full codebase-intelligence file list.

## Outputs
Something.
"""

_DRIFTED_SKILL_MD = """# Fake Skill

## Preconditions
- Nothing required.

## Required Context
None.

## Outputs
Something.
"""


def _write_skill(tmp_path, skill_name, skill_md_text):
    skill_dir = tmp_path / skill_name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(skill_md_text, encoding="utf-8")
    return skill_dir


def _template_for(skill_name):
    return WorkflowTemplate(
        name="t",
        description="d",
        steps=[
            WorkflowStep(
                skill_name="codebase-intelligence",
                output_filename="report.json",
                wiring_mode=WiringMode.CLI_FLAG,
            ),
            WorkflowStep(
                skill_name=skill_name,
                output_filename="out.json",
                wiring_mode=WiringMode.CLI_FLAG,
                wiring_flag="--ci-report",
                upstream_context_marker="codebase-intelligence",
            ),
        ],
    )


def test_no_issue_when_marker_present(tmp_path):
    _write_skill(tmp_path, "fake-skill", _GOOD_SKILL_MD)
    issues = check_template(_template_for("fake-skill"), tmp_path)
    assert issues == []


def test_issue_when_marker_missing(tmp_path):
    _write_skill(tmp_path, "fake-skill", _DRIFTED_SKILL_MD)
    issues = check_template(_template_for("fake-skill"), tmp_path)
    assert len(issues) == 1
    assert issues[0].step_skill_name == "fake-skill"


def test_issue_when_skill_md_missing(tmp_path):
    issues = check_template(_template_for("nonexistent-skill"), tmp_path)
    assert len(issues) == 1
    assert "not found" in issues[0].detail


def test_first_step_with_no_marker_is_never_checked(tmp_path):
    _write_skill(tmp_path, "fake-skill", _GOOD_SKILL_MD)
    issues = check_template(_template_for("fake-skill"), tmp_path)
    skill_names_checked = {issue.step_skill_name for issue in issues}
    assert "codebase-intelligence" not in skill_names_checked
