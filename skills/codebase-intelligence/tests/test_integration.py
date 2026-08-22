import json
from pathlib import Path

from engine.render_json import render_json
from engine.render_markdown import render_markdown
from engine.report import build_report


def test_full_pipeline_produces_valid_json_and_markdown(tmp_path: Path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "pkg" / "core.py").write_text('"""Core."""\ndef run():\n    pass\n', encoding="utf-8")
    (tmp_path / "pkg" / "cli.py").write_text("from . import core\ncore.run()\n", encoding="utf-8")
    (tmp_path / "requirements.txt").write_text("requests==2.31.0\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=do-not-leak\n", encoding="utf-8")

    report = build_report(tmp_path)
    json_output = render_json(report)
    markdown_output = render_markdown(report)

    parsed = json.loads(json_output)
    assert parsed["file_count"] == 4  # __init__.py, core.py, cli.py, requirements.txt (not .env)
    assert "do-not-leak" not in json_output
    assert "do-not-leak" not in markdown_output
    assert "requests" in json_output
    assert "# Codebase Intelligence Report" in markdown_output
