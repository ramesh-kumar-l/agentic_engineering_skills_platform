# Case 02 — multi-package-python

- **Input**: `fixtures/multi-package-python/` (a package with `__init__.py`, `utils.py`,
  `core.py` depending on `utils` via `from . import utils`, `cli.py` depending on
  `core` via `from . import core`, plus a `requirements.txt`).
- **Context**: Tests relative-import resolution (`from . import X` with `node.module is None`)
  and multi-hop internal dependency graph construction.
- **Expected Behavior**: Engine resolves both relative imports to real internal
  edges, detects `cli.py` as the sole entry point (only file with a main guard),
  and extracts `requests` from `requirements.txt`.
- **Acceptance Criteria**: `file_count == 5`; `internal_edges` contains exactly
  `[["pkg/core.py","pkg/utils.py"], ["pkg/cli.py","pkg/core.py"]]`;
  `entry_point_paths == ["pkg/cli.py"]`; `external_dependency_names == ["requests"]`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: bare relative import (`from . import X`, no `node.module`)
  silently dropped; level-1 vs level-2 relative import miscomputed; `__init__.py`
  not indexed for resolution.
