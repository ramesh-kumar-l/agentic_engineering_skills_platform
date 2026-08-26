from engine.memory_bank_parser import parse_decisions, parse_limitations
from engine.models import RecordStatus


def test_parse_decisions_basic(tmp_path):
    path = tmp_path / "decisions.md"
    path.write_text(
        "# Decisions\n"
        "\n"
        "## ADR-001: Adopt the thing\n"
        "Some body text mentioning `engine/scanner.py`.\n"
        "\n"
        "## ADR-002: Do another thing\n"
        "Different body.\n",
        encoding="utf-8",
    )
    records = parse_decisions(path)
    assert [r.record_id for r in records] == ["ADR-001", "ADR-002"]
    assert records[0].title == "Adopt the thing"
    assert records[0].record_type == "decision"
    assert records[0].mentioned_modules == ["engine/scanner.py"]
    assert records[0].status == RecordStatus.ACTIVE
    assert records[1].body == "Different body."


def test_parse_limitations_fixed_status(tmp_path):
    path = tmp_path / "limitations.md"
    path.write_text(
        "## L1: Something broke (FIXED during Phase 1)\n"
        "Body text.\n",
        encoding="utf-8",
    )
    records = parse_limitations(path)
    assert len(records) == 1
    assert records[0].record_id == "L1"
    assert records[0].status == RecordStatus.FIXED


def test_parse_limitations_skips_update_subentries(tmp_path):
    path = tmp_path / "limitations.md"
    path.write_text(
        "## L8: Judgment-layer evaluation is single-rater\n"
        "Body one.\n"
        "\n"
        "## L8 update: now applying a fourth time\n"
        "This should not become its own record.\n"
        "\n"
        "## L9: No runtime execution\n"
        "Body two.\n",
        encoding="utf-8",
    )
    records = parse_limitations(path)
    assert [r.record_id for r in records] == ["L8", "L9"]
    assert "update" not in records[0].body.lower()


def test_source_line_is_header_line_number(tmp_path):
    path = tmp_path / "decisions.md"
    path.write_text(
        "# Title\n"
        "\n"
        "## ADR-001: First\n"
        "Body.\n",
        encoding="utf-8",
    )
    records = parse_decisions(path)
    assert records[0].source_line == 3


def test_superseded_status_detected(tmp_path):
    path = tmp_path / "limitations.md"
    path.write_text("## L5: Old approach (SUPERSEDED by L6)\nBody.\n", encoding="utf-8")
    records = parse_limitations(path)
    assert records[0].status == RecordStatus.SUPERSEDED


def test_no_mentioned_modules_when_no_backticks(tmp_path):
    path = tmp_path / "decisions.md"
    path.write_text("## ADR-001: First\nNo code here at all.\n", encoding="utf-8")
    records = parse_decisions(path)
    assert records[0].mentioned_modules == []


def test_empty_file_returns_no_records(tmp_path):
    path = tmp_path / "decisions.md"
    path.write_text("# Just a title, no sections\n", encoding="utf-8")
    assert parse_decisions(path) == []


def test_duplicate_backtick_mention_deduplicated(tmp_path):
    path = tmp_path / "decisions.md"
    path.write_text(
        "## ADR-001: First\n"
        "See `engine/scanner.py` and later `engine/scanner.py` again.\n",
        encoding="utf-8",
    )
    records = parse_decisions(path)
    assert records[0].mentioned_modules == ["engine/scanner.py"]
