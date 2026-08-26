from engine.operation_parser import parse_operation, parse_operation_type, parse_targets


def test_detects_rename():
    assert parse_operation_type("Rename `foo.py` to `bar.py`.") == "rename"


def test_detects_delete():
    assert parse_operation_type("Delete the legacy `old_helper` function.") == "delete"
    assert parse_operation_type("Remove `old_helper`.") == "delete"


def test_detects_move():
    assert parse_operation_type("Move `utils.py` into the `core/` package.") == "move"


def test_detects_change_signature():
    assert parse_operation_type("Change the signature of `build_report`.") == "change-signature"


def test_detects_split():
    assert parse_operation_type("Split `services.py` into smaller modules.") == "split"


def test_detects_merge():
    assert parse_operation_type("Merge `a.py` and `b.py` into one module.") == "merge"


def test_detects_extract():
    assert parse_operation_type("Extract a helper from `report.py`.") == "extract"


def test_detects_inline():
    assert parse_operation_type("Inline the `_helper` function into its caller.") == "inline"


def test_falls_back_to_generic_refactor():
    assert parse_operation_type("Clean up `report.py` a bit.") == "refactor"


def test_extracts_backtick_targets():
    targets = parse_targets("Rename `foo.py` to `bar.py`.")
    names = [t.name for t in targets]
    assert names == ["foo.py", "bar.py"]


def test_extracts_quoted_targets():
    targets = parse_targets("Rename 'foo.py' to 'bar.py'.")
    names = [t.name for t in targets]
    assert names == ["foo.py", "bar.py"]


def test_falls_back_to_bare_identifiers_when_no_quotes():
    targets = parse_targets("Rename build_report to construct_report.")
    names = [t.name for t in targets]
    assert "build_report" in names
    assert "construct_report" in names


def test_bare_identifier_extraction_excludes_operation_keywords():
    targets = parse_targets("Rename the report_builder module.")
    names = [t.name for t in targets]
    assert "report_builder" in names
    assert "rename" not in names
    assert "module" not in names


def test_empty_text_yields_no_targets():
    assert parse_targets("") == []


def test_parse_operation_returns_both():
    op_type, targets = parse_operation("Rename `foo.py` to `bar.py`.")
    assert op_type == "rename"
    assert len(targets) == 2
