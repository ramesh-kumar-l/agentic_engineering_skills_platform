"""Resolves each parsed RefactorTarget against a real codebase-intelligence
report: is this actually a module, a function, or a class that exists in
the target repo — and if so, who structurally depends on it?

Resolution order mirrors how a reader would recognize the name: an exact
module path/stem match first (the target names a file), then a function or
class name defined somewhere in the report (the target names a symbol
inside some module), else left unresolved — an unresolved target is not
silently dropped, it is reported as-is so the agent's Step 3 walk can flag
that the refactor names something this repo's structural map doesn't
recognize (a typo, a not-yet-created file, or a different repo entirely).

Caller resolution: a module "calls" a target module if the target's path or
stem appears anywhere in that module's raw `imports` list — the same
substring-matching discipline feature-planner's relevance_scorer.py and
architecture-decision's impact_scorer.py already use for this project's
lightweight, AST-free import representation.
"""

from __future__ import annotations

import re
from pathlib import PurePosixPath

from .models import CallerModule, CiReportContext, RefactorTarget, TargetAssessment


def _stem(path: str) -> str:
    return PurePosixPath(path).stem


def _contains_whole_token(haystack: str, needle: str) -> bool:
    """Word-boundary-aware containment check.

    A bare `needle in haystack` substring check false-positives whenever
    `needle` (a module stem like "scanner") happens to appear inside a
    longer, unrelated identifier (e.g. "testability_scanner") — see L14/
    L19/L21/L23 in project-memory-bank/12-known-limitations.md. Since `\\w`
    includes `_`, `\\bscanner\\b` correctly rejects "testability_scanner"
    (no boundary between "_" and "s") while still matching "engine.scanner"
    (boundary at ".").
    """
    if not needle:
        return False
    return re.search(rf"\b{re.escape(needle)}\b", haystack) is not None


def _resolve_module(name: str, ci_report: CiReportContext):
    lowered = name.lower()
    for module in ci_report.modules:
        if _stem(module.path).lower() == lowered:
            return module
        if module.path.lower().endswith("/" + lowered) or module.path.lower() == lowered:
            return module
    return None


def _resolve_symbol(name: str, ci_report: CiReportContext):
    for module in ci_report.modules:
        if name in module.functions or name in module.classes:
            return module
    return None


def _find_callers(resolved_path: str, ci_report: CiReportContext) -> list[CallerModule]:
    target_stem = _stem(resolved_path).lower()
    callers: list[CallerModule] = []
    for module in ci_report.modules:
        if module.path == resolved_path:
            continue
        imports_text = " ".join(module.imports).lower()
        if _contains_whole_token(imports_text, target_stem) or _contains_whole_token(
            imports_text, resolved_path.lower()
        ):
            callers.append(
                CallerModule(
                    path=module.path,
                    fan_in=ci_report.dependency_graph.fan_in.get(module.path, 0),
                    fan_out=ci_report.dependency_graph.fan_out.get(module.path, 0),
                    is_hotspot=module.path in ci_report.dependency_graph.hotspots,
                )
            )
    return callers


def resolve_target(target: RefactorTarget, ci_report: CiReportContext) -> TargetAssessment:
    module = _resolve_module(target.name, ci_report)
    matched_functions: list[str] = []
    matched_classes: list[str] = []

    if module is None:
        symbol_module = _resolve_symbol(target.name, ci_report)
        if symbol_module is not None:
            module = symbol_module
            if target.name in symbol_module.functions:
                matched_functions.append(target.name)
            if target.name in symbol_module.classes:
                matched_classes.append(target.name)

    if module is None:
        return TargetAssessment(target_name=target.name, resolved_module_path=None)

    fan_in = ci_report.dependency_graph.fan_in.get(module.path, 0)
    fan_out = ci_report.dependency_graph.fan_out.get(module.path, 0)
    is_hotspot = module.path in ci_report.dependency_graph.hotspots
    callers = _find_callers(module.path, ci_report)

    return TargetAssessment(
        target_name=target.name,
        resolved_module_path=module.path,
        matched_functions=matched_functions,
        matched_classes=matched_classes,
        fan_in=fan_in,
        fan_out=fan_out,
        is_hotspot=is_hotspot,
        caller_modules=callers,
    )


def resolve_targets(
    targets: list[RefactorTarget], ci_report: CiReportContext
) -> list[TargetAssessment]:
    return [resolve_target(target, ci_report) for target in targets]
