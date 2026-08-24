"""Resolves each diff-changed file's effective path against a real
codebase-intelligence report: is this actually a known module, and if so,
who structurally depends on it?

Independent copy of refactoring-safety's/regression-hunter's
target_resolver.py resolution discipline (ADR-013/ADR-014/ADR-015 lineage):
an exact path match first, then a module-stem match as a fallback. An
unresolved file is not silently dropped — it is reported as-is
(structural_tier stays "low", fan_in/fan_out stay 0) so the agent's Step 3
walk can see that the composed report has no structural data for it.

Caller resolution reuses the SAME substring-matching heuristic already
disclosed as L23 in project-memory-bank/12-known-limitations.md
(`target_stem in imports_text`) — this is a THIRD independent copy of that
exact limitation (after refactoring-safety's and regression-hunter's), not a
new bug. It is disclosed again here (see SKILL.md's Known Limitations) with
an explicit cross-reference to L23 rather than a new L-number, since it is
the same underlying issue, not a new finding.
"""

from __future__ import annotations

from pathlib import PurePosixPath

from .models import CallerModule, CiReportContext, StructuralAssessment


def _stem(path: str) -> str:
    return PurePosixPath(path).stem


def _resolve_module(path: str, ci_report: CiReportContext):
    lowered = path.lower()
    for module in ci_report.modules:
        if module.path.lower() == lowered:
            return module
    target_stem = _stem(path).lower()
    for module in ci_report.modules:
        if _stem(module.path).lower() == target_stem:
            return module
    return None


def _find_callers(resolved_path: str, ci_report: CiReportContext) -> list[CallerModule]:
    target_stem = _stem(resolved_path).lower()
    callers: list[CallerModule] = []
    for module in ci_report.modules:
        if module.path == resolved_path:
            continue
        imports_text = " ".join(module.imports).lower()
        if target_stem in imports_text or resolved_path.lower() in imports_text:
            callers.append(
                CallerModule(
                    path=module.path,
                    fan_in=ci_report.dependency_graph.fan_in.get(module.path, 0),
                    fan_out=ci_report.dependency_graph.fan_out.get(module.path, 0),
                    is_hotspot=module.path in ci_report.dependency_graph.hotspots,
                )
            )
    return callers


def resolve_file(
    effective_path: str | None, ci_report: CiReportContext
) -> StructuralAssessment:
    if effective_path is None:
        return StructuralAssessment()

    module = _resolve_module(effective_path, ci_report)
    if module is None:
        return StructuralAssessment()

    fan_in = ci_report.dependency_graph.fan_in.get(module.path, 0)
    fan_out = ci_report.dependency_graph.fan_out.get(module.path, 0)
    is_hotspot = module.path in ci_report.dependency_graph.hotspots
    callers = _find_callers(module.path, ci_report)

    return StructuralAssessment(
        resolved_module_path=module.path,
        fan_in=fan_in,
        fan_out=fan_out,
        is_hotspot=is_hotspot,
        caller_modules=callers,
    )
