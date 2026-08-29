"""Condensed, human/agent-readable Markdown rendering.

Deliberately summarized (top hotspots, not every file) so the output stays
"minimum sufficient context" even for large repos — see NFR2 in
project-memory-bank/02-requirements.md. Full detail belongs in the JSON
output (render_json.py), not here.
"""

from __future__ import annotations

from .models import CodebaseIntelligenceReport

TOP_N_HOTSPOTS = 10
TOP_N_UNDOCUMENTED_DIRS = 10


def render_markdown(report: CodebaseIntelligenceReport) -> str:
    lines: list[str] = []
    lines.append(f"# Codebase Intelligence Report")
    lines.append("")
    lines.append(f"- Root: `{report.root_path}`")
    lines.append(f"- Generated: {report.generated_at}")
    lines.append(f"- Files scanned: {report.file_count} "
                  f"(excluded dirs: {report.excluded_dir_count}, skipped files: {report.skipped_file_count})")
    lines.append("")

    lines.append("## Language breakdown")
    for lang, count in sorted(report.language_breakdown.items(), key=lambda kv: -kv[1]):
        lines.append(f"- {lang}: {count}")
    lines.append("")

    lines.append("## Entry points")
    if report.entry_points:
        for ep in report.entry_points:
            lines.append(f"- `{ep.path}` ({ep.reason})")
    else:
        lines.append("_None detected._")
    lines.append("")

    lines.append(f"## Internal dependency hotspots (top {TOP_N_HOTSPOTS})")
    lines.append("Modules with the most internal fan-in + fan-out — likely the highest-blast-radius files to change.")
    if report.dependency_graph.hotspots:
        for node in report.dependency_graph.hotspots[:TOP_N_HOTSPOTS]:
            fan_in = report.dependency_graph.fan_in.get(node, 0)
            fan_out = report.dependency_graph.fan_out.get(node, 0)
            lines.append(f"- `{node}` — depended on by {fan_in}, depends on {fan_out}")
    else:
        lines.append("_No internal dependency edges detected._")
    lines.append("")

    lines.append("## External dependencies")
    if report.external_dependencies:
        by_source: dict[str, list[str]] = {}
        for d in report.external_dependencies:
            label = f"{d.name}{(' ' + d.version) if d.version else ''}"
            by_source.setdefault(d.source_file, []).append(label)
        for source, names in by_source.items():
            lines.append(f"- {source}: {', '.join(sorted(names))}")
    else:
        lines.append(
            "_None found (no requirements.txt / pyproject.toml / package.json / "
            "pom.xml / build.gradle[.kts])._"
        )
    lines.append("")

    lines.append(f"## Directories missing a README (top {TOP_N_UNDOCUMENTED_DIRS})")
    if report.doc_coverage.dirs_without_readme:
        for d in report.doc_coverage.dirs_without_readme[:TOP_N_UNDOCUMENTED_DIRS]:
            lines.append(f"- `{d or '.'}`")
    else:
        lines.append("_Every directory with files has a README._")
    lines.append("")

    if report.warnings:
        lines.append("## Warnings")
        for w in report.warnings[:20]:
            lines.append(f"- {w}")
        if len(report.warnings) > 20:
            lines.append(f"- ...and {len(report.warnings) - 20} more")
        lines.append("")

    return "\n".join(lines)
