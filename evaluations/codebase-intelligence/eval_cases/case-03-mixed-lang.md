# Case 03 — mixed-lang

- **Input**: `fixtures/mixed-lang/` (a Python file, a small JS pair with a relative
  `require('./utils')`, a `package.json` with one dependency, and a `node_modules/`
  directory that must be excluded).
- **Context**: Tests the heuristic (non-AST) JS import resolver, cross-language
  language-breakdown counting, `package.json` external-dependency parsing, and
  directory exclusion.
- **Expected Behavior**: `node_modules/` and its contents are excluded entirely
  (not scanned, not counted in `file_count`); the JS relative import resolves to
  an internal edge; `lodash` is extracted as an external dependency.
- **Acceptance Criteria**: `file_count == 4`; `excluded_dir_count == 1`;
  `internal_edges == [["client/index.js","client/utils.js"]]`;
  `external_dependency_names == ["lodash"]`.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: `node_modules` files leaking into the report;
  bare specifier (e.g. a future `require('lodash')`) incorrectly treated as
  internal; JS relative-path resolution missing the file extension.
