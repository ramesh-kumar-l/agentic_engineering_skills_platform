"""Thin CLI entry point. All real logic lives in executor.py and the
workflow registry.

Usage:
    python -m engine.cli <template-name> --repo-path <dir> --task "<text>" \
        --out-dir <dir> [--dry-run] [--format json|markdown|both]
    python -m engine.cli --list-templates

Runs a hardcoded, previously-dogfooded chain of real skill CLIs against a
target repo (see workflow_registry.py) — the first skill in this
portfolio whose deliverable is composed execution, not analysis.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .executor import run_workflow
from .render_json import render_json
from .render_markdown import render_markdown
from .workflow_registry import REGISTRY, get_template, list_templates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="workflow-composer", description=__doc__)
    parser.add_argument(
        "template", nargs="?", default=None,
        help="Registered workflow template name (see --list-templates).",
    )
    parser.add_argument("--repo-path", type=Path, default=None,
                         help="Path to the repository the workflow analyzes.")
    parser.add_argument("--task", default=None,
                         help="Free-text task description passed to downstream steps.")
    parser.add_argument("--out-dir", type=Path, default=None,
                         help="Directory to write per-step outputs and the run report into.")
    parser.add_argument("--dry-run", action="store_true",
                         help="Validate the plan without spawning any subprocess.")
    parser.add_argument("--format", choices=["json", "markdown", "both"], default="both")
    parser.add_argument("--list-templates", action="store_true",
                         help="Print the registered templates and exit.")
    args = parser.parse_args(argv)

    if args.list_templates:
        for template in list_templates():
            print(f"{template.name}: {template.description}")
        return 0

    if args.template is None:
        print("error: a template name is required (see --list-templates)", file=sys.stderr)
        return 1

    template = get_template(args.template)
    if template is None:
        known = ", ".join(sorted(REGISTRY))
        print(f"error: unknown template '{args.template}' (known: {known})", file=sys.stderr)
        return 1

    if args.repo_path is None or not args.repo_path.exists():
        print(f"error: --repo-path is required and must exist: {args.repo_path}", file=sys.stderr)
        return 1
    if not args.dry_run and not args.task:
        print("error: --task is required unless --dry-run is set", file=sys.stderr)
        return 1
    if args.out_dir is None:
        print("error: --out-dir is required", file=sys.stderr)
        return 1

    args.out_dir.mkdir(parents=True, exist_ok=True)
    report = run_workflow(
        template,
        repo_path=args.repo_path,
        task_description=args.task or "",
        out_dir=args.out_dir,
        dry_run=args.dry_run,
    )

    outputs: dict[str, str] = {}
    if args.format in ("json", "both"):
        outputs["workflow-run-report.json"] = render_json(report)
    if args.format in ("markdown", "both"):
        outputs["workflow-run-report.md"] = render_markdown(report)

    for filename, content in outputs.items():
        (args.out_dir / filename).write_text(content, encoding="utf-8")
        print(f"wrote {args.out_dir / filename}")

    any_failed = any(r.status.value == "FAILED" for r in report.step_results)
    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
