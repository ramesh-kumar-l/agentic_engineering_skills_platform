"""Resolves a memory record's mentioned module references against a real
codebase-intelligence report — confirms the module still exists in the
current repo, and surfaces its structural significance (hotspot / fan_in)
when it does.

Whole-token basename EQUALITY, never substring containment, applied from
day one. This project has disclosed the same coincidental-substring-
flooding mechanism class six times across five skills (L14, L19, L21,
L23/L24, L28, L29, L30 — project-memory-bank/12-known-limitations.md).
engineering-memory is the first skill built with the benefit of all six
prior occurrences known in advance: comparing basenames for exact
equality (not `stem in path`) means a short/common stem like "io.py" can
never match "studio.py" or any other unrelated file that merely contains
the substring — there is no containment check here at all to have that
failure mode. Disclosed as "mitigated by construction, not proven
bug-free" in SKILL.md Known Limitations — see there for the residual gap
(two different real repo paths sharing an identical basename resolve
ambiguously to whichever the CI report lists, not to a chosen "correct"
one).
"""

from __future__ import annotations

from pathlib import PurePosixPath

from .models import CiReportContext, ModuleFlag


def _basename(token: str) -> str:
    return PurePosixPath(token).name


def resolve_module_mentions(
    mentioned_modules: list[str], ci_report: CiReportContext
) -> list[ModuleFlag]:
    """One ModuleFlag per mentioned module string, in order. `exists` is
    True only when a CI-report module's own basename matches exactly."""
    by_basename: dict[str, tuple[str, int, bool]] = {}
    for module in ci_report.modules:
        base = _basename(module.path)
        is_hotspot = module.path in ci_report.dependency_graph.hotspots
        fan_in = ci_report.dependency_graph.fan_in.get(module.path, 0)
        by_basename[base] = (module.path, fan_in, is_hotspot)

    flags: list[ModuleFlag] = []
    for mention in mentioned_modules:
        found = by_basename.get(_basename(mention))
        if found is None:
            flags.append(ModuleFlag(module_path=mention, exists=False))
        else:
            path, fan_in, is_hotspot = found
            flags.append(
                ModuleFlag(module_path=path, exists=True, is_hotspot=is_hotspot, fan_in=fan_in)
            )
    return flags
