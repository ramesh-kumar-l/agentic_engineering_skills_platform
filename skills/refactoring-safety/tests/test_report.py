import json

from engine.report import build_report

SAMPLE = {
    "root_path": "/repo",
    "modules": [
        {
            "path": "engine/report.py",
            "docstring": "Builds the report.",
            "functions": ["build_report"],
            "classes": [],
            "imports": [],
        },
        {
            "path": "engine/cli.py",
            "docstring": "CLI entry point.",
            "functions": ["main"],
            "classes": [],
            "imports": ["engine.report"],
        },
    ],
    "dependency_graph": {
        "fan_in": {"engine/report.py": 6},
        "fan_out": {},
        "hotspots": ["engine/report.py"],
    },
}


def _write_ci_report(tmp_path) -> str:
    path = tmp_path / "ci-report.json"
    path.write_text(json.dumps(SAMPLE), encoding="utf-8")
    return str(path)


def test_build_report_resolves_target_and_scores_risk(tmp_path):
    report = build_report(
        "Rename `report.py` to `builder.py`.", _write_ci_report(tmp_path)
    )
    assert report.operation_type == "rename"
    assert report.targets[0].resolved_module_path == "engine/report.py"
    assert report.targets[0].risk_tier == "high"


def test_empty_text_warns(tmp_path):
    report = build_report("", _write_ci_report(tmp_path))
    assert any("empty" in w.lower() for w in report.warnings)


def test_no_targets_parsed_warns(tmp_path):
    report = build_report("Clean things up a bit.", _write_ci_report(tmp_path))
    assert any("No target identifiers" in w for w in report.warnings)


def test_unresolved_targets_warn(tmp_path):
    report = build_report("Rename `nope.py` to `also_nope.py`.", _write_ci_report(tmp_path))
    assert any("did not match" in w.lower() or "none of the parsed targets" in w.lower() for w in report.warnings)


def test_high_risk_target_warns(tmp_path):
    report = build_report("Rename `report.py`.", _write_ci_report(tmp_path))
    assert any("HIGH" in w for w in report.warnings)


def test_untested_blast_radius_warns(tmp_path):
    report = build_report("Rename `report.py`.", _write_ci_report(tmp_path))
    assert any("unverified" in w for w in report.warnings)


def test_report_never_fabricates_a_verdict(tmp_path):
    from engine.render_json import render_json

    report = build_report("Rename `report.py`.", _write_ci_report(tmp_path))
    parsed = json.loads(render_json(report))
    assert "decision" not in parsed
    assert "approved" not in parsed
    assert "safe_to_proceed" not in parsed
