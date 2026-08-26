"""Deterministic drift guard between a template's declared wiring and the
real SKILL.md contract of the skill it targets.

This is a textual drift check, not real schema/type validation (disclosed
in SKILL.md Known Limitations): it confirms the upstream skill's name
still appears in the downstream skill's "Preconditions"/"Required
Context" sections. If a future edit to a skill's SKILL.md drops that
mention without updating this registry, real execution refuses to proceed
past the flagged issue (fails closed).
"""

from __future__ import annotations

import re
from pathlib import Path

from .models import CompatibilityIssue, WorkflowTemplate

_SECTION_NAMES = ("Preconditions", "Required Context")


def _extract_sections(skill_md_text: str, section_names: tuple[str, ...]) -> str:
    """Return the concatenated text of the named '## <name>' sections."""
    chunks: list[str] = []
    for name in section_names:
        pattern = re.compile(
            rf"^##\s+{re.escape(name)}\s*$(.*?)(?=^##\s+|\Z)",
            re.MULTILINE | re.DOTALL,
        )
        match = pattern.search(skill_md_text)
        if match:
            chunks.append(match.group(1))
    return "\n".join(chunks)


def check_template(
    template: WorkflowTemplate, skills_root: Path
) -> list[CompatibilityIssue]:
    issues: list[CompatibilityIssue] = []
    for step in template.steps:
        if step.upstream_context_marker is None:
            continue
        skill_md = skills_root / step.skill_name / "SKILL.md"
        if not skill_md.exists():
            issues.append(
                CompatibilityIssue(
                    step_skill_name=step.skill_name,
                    detail=f"SKILL.md not found at {skill_md}",
                )
            )
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        section_text = _extract_sections(text, _SECTION_NAMES)
        if step.upstream_context_marker not in section_text:
            issues.append(
                CompatibilityIssue(
                    step_skill_name=step.skill_name,
                    detail=(
                        f"expected '{step.upstream_context_marker}' to appear in "
                        f"{step.skill_name}/SKILL.md's Preconditions/Required "
                        f"Context sections, but it does not — declared wiring "
                        f"may be stale"
                    ),
                )
            )
    return issues
