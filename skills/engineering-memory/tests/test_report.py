import json

from engine.report import build_report


def _write_ci_report(tmp_path, modules=None, fan_in=None, hotspots=None):
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps({
        "root_path": "/repo",
        "modules": modules or [],
        "dependency_graph": {"fan_in": fan_in or {}, "fan_out": {}, "hotspots": hotspots or []},
    }), encoding="utf-8")
    return path


def _write_decisions(tmp_path, text=""):
    path = tmp_path / "decisions.md"
    path.write_text(text, encoding="utf-8")
    return path


def _write_limitations(tmp_path, text=""):
    path = tmp_path / "limitations.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_empty_task_adds_warning(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path, "## ADR-001: First\nBody.\n")
    limitations = _write_limitations(tmp_path)
    report = build_report("   ", str(ci_report), str(decisions), str(limitations))
    assert any("empty" in w.lower() for w in report.warnings)


def test_empty_corpus_adds_warning(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path)
    limitations = _write_limitations(tmp_path)
    report = build_report("fix the scanner", str(ci_report), str(decisions), str(limitations))
    assert any("no records parsed" in w.lower() for w in report.warnings)


def test_relevant_task_surfaces_matching_record_not_unrelated_one(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path, "## ADR-001: Scanner design\nDiscusses the scanner.\n")
    limitations = _write_limitations(
        tmp_path, "## L1: Unrelated parsing gap\nNothing to do with scanners.\n"
    )
    report = build_report(
        "we need to fix the scanner", str(ci_report), str(decisions), str(limitations)
    )
    ids = [m.record.record_id for m in report.matches]
    assert "ADR-001" in ids
    assert "L1" not in ids


def test_top_n_limits_matches(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions_text = "\n".join(
        f"## ADR-{i:03d}: scanner topic {i}\nBody about scanner.\n" for i in range(1, 6)
    )
    decisions = _write_decisions(tmp_path, decisions_text)
    limitations = _write_limitations(tmp_path)
    report = build_report(
        "scanner", str(ci_report), str(decisions), str(limitations), top_n=2
    )
    assert len(report.matches) == 2


def test_fixed_record_still_surfaces_but_flagged_stale(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(tmp_path)
    limitations = _write_limitations(
        tmp_path, "## L1: scanner bug (FIXED during Phase 1)\nThe scanner had a bug.\n"
    )
    report = build_report("scanner bug", str(ci_report), str(decisions), str(limitations))
    assert len(report.matches) == 1
    assert report.matches[0].staleness.is_stale is True


def test_module_mention_resolved_against_ci_report(tmp_path):
    ci_report = _write_ci_report(
        tmp_path,
        modules=[{"path": "engine/scanner.py", "docstring": None, "functions": [], "classes": [], "imports": []}],
        fan_in={"engine/scanner.py": 5},
        hotspots=["engine/scanner.py"],
    )
    decisions = _write_decisions(
        tmp_path, "## ADR-001: Scanner rewrite\nSee `engine/scanner.py` for details.\n"
    )
    limitations = _write_limitations(tmp_path)
    report = build_report(
        "rewriting the scanner", str(ci_report), str(decisions), str(limitations)
    )
    match = report.matches[0]
    assert "engine/scanner.py" in match.matched_modules


def test_matches_sorted_by_descending_score(tmp_path):
    ci_report = _write_ci_report(tmp_path)
    decisions = _write_decisions(
        tmp_path,
        "## ADR-001: scanner\nscanner scanner scanner.\n"
        "\n"
        "## ADR-002: scanner mention\nBody with a single scanner reference.\n",
    )
    limitations = _write_limitations(tmp_path)
    report = build_report("scanner", str(ci_report), str(decisions), str(limitations))
    scores = [m.score for m in report.matches]
    assert scores == sorted(scores, reverse=True)
