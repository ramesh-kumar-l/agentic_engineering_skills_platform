"""End-to-end: a realistic task composed with a real-shaped CI report and
memory-bank fixture text, confirming parsing, module resolution, relevance
scoring, and staleness classification compose correctly through the full
pipeline."""

import json

from engine.report import build_report


def test_full_pipeline_on_realistic_memory_bank_fixture(tmp_path):
    ci_report = tmp_path / "ci-report.json"
    ci_report.write_text(json.dumps({
        "root_path": "/repo",
        "modules": [
            {"path": "engine/target_resolver.py", "docstring": None,
             "functions": [], "classes": [], "imports": []},
        ],
        "dependency_graph": {
            "fan_in": {"engine/target_resolver.py": 6},
            "fan_out": {},
            "hotspots": ["engine/target_resolver.py"],
        },
    }), encoding="utf-8")

    decisions = tmp_path / "decisions.md"
    decisions.write_text(
        "## ADR-010: feature-planner requires a codebase-intelligence report\n"
        "A required-composition pattern, later reused across many skills.\n"
        "\n"
        "## ADR-018: engineering-knowledge-capture builds its resolver correct from day one\n"
        "Uses `engine/target_resolver.py`'s word-boundary fix as precedent.\n",
        encoding="utf-8",
    )

    limitations = tmp_path / "limitations.md"
    limitations.write_text(
        "## L23: target_resolver.py's substring-based caller identification "
        "produces a wildly inflated caller list (FIXED 2026-08-26, mentor-review follow-up)\n"
        "See `engine/target_resolver.py`.\n",
        encoding="utf-8",
    )

    report = build_report(
        "we're building a resolver that must avoid target_resolver.py's substring bug",
        str(ci_report), str(decisions), str(limitations),
    )

    ids = [m.record.record_id for m in report.matches]
    assert "L23" in ids
    assert "ADR-018" in ids

    l23 = next(m for m in report.matches if m.record.record_id == "L23")
    assert l23.staleness.is_stale is True
    assert "engine/target_resolver.py" in l23.matched_modules

    assert report.warnings == []
