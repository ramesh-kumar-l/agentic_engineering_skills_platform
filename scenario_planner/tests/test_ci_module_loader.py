import json

import pytest

from scenario_planner.ci_module_loader import CiModuleLoadError, load_ci_modules

_VALID = {
    "modules": [
        {
            "path": "pkg/module.py",
            "functions": ["foo", "bar"],
            "classes": ["Baz"],
        },
        {"path": "pkg/empty.py", "functions": [], "classes": []},
    ]
}


def test_loads_modules_keyed_by_path(tmp_path):
    path = tmp_path / "ci.json"
    path.write_text(json.dumps(_VALID), encoding="utf-8")

    modules = load_ci_modules(path)

    assert modules["pkg/module.py"].functions == ["foo", "bar"]
    assert modules["pkg/module.py"].classes == ["Baz"]
    assert modules["pkg/empty.py"].functions == []


def test_missing_file_raises_ci_module_load_error(tmp_path):
    with pytest.raises(CiModuleLoadError):
        load_ci_modules(tmp_path / "missing.json")


def test_missing_modules_key_raises_ci_module_load_error(tmp_path):
    path = tmp_path / "ci.json"
    path.write_text(json.dumps({}), encoding="utf-8")

    with pytest.raises(CiModuleLoadError):
        load_ci_modules(path)


def test_module_missing_path_raises_ci_module_load_error(tmp_path):
    path = tmp_path / "ci.json"
    bad = {"modules": [{"functions": []}]}
    path.write_text(json.dumps(bad), encoding="utf-8")

    with pytest.raises(CiModuleLoadError):
        load_ci_modules(path)


def test_wrong_type_modules_raises_ci_module_load_error(tmp_path):
    path = tmp_path / "ci.json"
    path.write_text(json.dumps({"modules": "oops"}), encoding="utf-8")

    with pytest.raises(CiModuleLoadError, match="must be a list"):
        load_ci_modules(path)


def test_non_dict_module_entry_raises_ci_module_load_error(tmp_path):
    path = tmp_path / "ci.json"
    path.write_text(json.dumps({"modules": ["pkg/module.py"]}), encoding="utf-8")

    with pytest.raises(CiModuleLoadError, match="not an object"):
        load_ci_modules(path)
