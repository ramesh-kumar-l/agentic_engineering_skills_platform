# 12 — Known Limitations

Running failure/limitation catalog. First entries from Phase 1
(codebase-intelligence). Format follows the failure-record structure in
[[05-evaluation-framework]]: What failed | Why | Impact | Fix | Regression prevention.

---

## L1: `has_main_guard` false-positive on string mentions (FIXED during Phase 1)

- **What failed**: Entry-point detection flagged files that merely contain the
  text `__name__ == "__main__"` inside a docstring, comment, or string literal
  as real CLI entry points.
- **Why**: Original implementation did a plain substring search over full file
  text instead of checking the AST for an actual top-level `if` statement.
- **Impact**: Found via dogfooding (running the engine on its own repo) —
  `engine/models.py`, `engine/report.py`, `engine/python_parser.py`, and two
  test files were misreported as entry points.
- **Fix**: Replaced with an AST check (`engine/python_parser.py::_has_main_guard`)
  that requires an actual top-level `ast.If` comparing `__name__` to the
  string `"__main__"`.
- **Regression prevention**: `tests/test_python_parser.py::test_has_main_guard_ignores_string_mentions`.

## L2: External dependency parsing is root-only, not recursive

- **What failed**: `external_deps.py` only checks the scan root directory for
  `requirements.txt`/`pyproject.toml`/`package.json` — it does not look for
  manifests in subdirectories.
- **Why**: Scoped down for Phase 1 to keep the module simple; monorepo/
  multi-package layouts weren't in the original fixture set.
- **Impact**: On a monorepo (e.g. this platform's own repo, where the real
  manifest lives at `skills/codebase-intelligence/pyproject.toml`, not root),
  the report shows zero external dependencies even though some exist deeper
  in the tree. Observed directly via dogfooding — see
  `examples/codebase-intelligence/example-run.md`.
- **Fix**: Not yet fixed — deferred. Revisit if/when a real user hits this on
  an actual monorepo (avoid over-engineering ahead of evidence, per
  [[05-evaluation-framework]]).
- **Regression prevention**: N/A yet — tracked here so it isn't silently
  forgotten or re-discovered from scratch later.

## L3: Non-Python import extraction is heuristic, not a real parser

- **What failed**: N/A (documented limitation, not an observed bug).
- **Why**: `generic_parser.py` uses regex patterns for JS/TS/Java imports
  rather than a real AST/parser for those languages.
- **Impact**: Will miss dynamic imports (`import(...)`), re-exports, and
  unusual formatting in non-Python files. JS internal-dependency resolution
  in `graph.py` only handles relative specifiers (`./`, `../`) — bundler path
  aliases (e.g. `@/utils`) are not resolved and will be (correctly) treated as
  external/unresolved.
- **Fix**: Not planned unless real usage shows this matters — multi-language
  AST parsing is a significant investment the assumptions ledger doesn't yet
  justify (see [[16-assumptions-and-validation]]).
- **Regression prevention**: Explicitly documented in `SKILL.md` ("When NOT to
  Use" / "Known Limitations") so agents don't over-trust non-Python results.

## L4: No semantic or cross-file type understanding

- **What failed**: N/A (scope boundary, not a bug).
- **Why**: The engine is intentionally structural only (imports, def/class
  names, docstrings) — this is a deliberate scope decision, not an oversight.
- **Impact**: Cannot answer "does function X actually call function Y" or
  "what type does this return" — only "does file A import file B."
- **Fix**: Out of scope for this skill; a future skill could build on this
  report rather than this skill absorbing that scope.
- **Regression prevention**: Documented in `SKILL.md` under "Context
  Completeness."

---

Entries below are from Phase 2 (adversarial-diff-reviewer).

## L5: Redaction only covered the `RiskFlag`, not the raw diff content (FIXED during Phase 2)

- **What failed**: The first implementation of `risk_scanner.scan()` computed
  a redacted `matched_text` for the `RiskFlag`, but left the actual secret
  literal untouched in the underlying `LineChange.content` — which is also
  serialized into `diff-report.json`/`diff-report.md`, so the secret still
  leaked through the raw diff content even though the flag itself was clean.
- **Why**: Redaction was implemented as a display-value computation for the
  flag, without considering that the parsed diff content is a second,
  independent output surface.
- **Impact**: Found by `tests/test_integration.py::test_secret_value_never_leaks_into_json_or_markdown`
  failing on first run — before this skill shipped, not after.
- **Fix**: `risk_scanner.py` now mutates `line.content` in place for
  `redact=True` pattern matches, so both output surfaces stay consistent.
- **Regression prevention**: the integration test above, still in the suite.

## L6: Redaction only covered the first occurrence per line (FIXED during Phase 2)

- **What failed**: After fixing L5, the redaction still used
  `pattern.regex.search()` + string slicing, which only finds and redacts the
  *first* match of a pattern on a line. A line with two secrets of the same
  shape (e.g. `api_key = "AAA"; token = "BBB"`, both matching the single
  `hardcoded-secret` pattern) would leak the second one.
- **Why**: `search()` returns one match; the fix didn't account for multiple
  occurrences of the same pattern within a single line.
- **Impact**: Found via adversarial self-review while building the dogfood
  example (`examples/adversarial-diff-reviewer/example-run.md`) — a real,
  non-hypothetical second-order bug in the L5 fix itself, caught by actually
  applying this skill's own Step 3 workflow to its own diff.
- **Fix**: Switched to `pattern.regex.sub()`, which redacts every occurrence
  of the pattern on the line in one pass.
- **Regression prevention**: `tests/test_risk_scanner.py::test_all_occurrences_of_a_secret_pattern_on_one_line_are_redacted`.

## L7: Risk-flag regexes only catch mechanically-shaped issues

- **What failed**: N/A (scope boundary, not a bug).
- **Why**: `risk_patterns.py` is a fixed table of regexes — it can only match
  syntactic shapes it was written to recognize.
- **Impact**: Will both over-flag (e.g. a legitimate `except Exception:` that
  logs and re-raises, not just `pass`) and under-flag (any defect not
  matching a known pattern — most subtle bugs, concurrency bugs, and logic
  errors, which is exactly why Step 3's agent-driven review exists as a
  separate layer; see `evaluations/adversarial-diff-reviewer/RESULTS.md` where
  6 of 8 fixtures have zero deterministic risk flags but a real seeded
  defect).
- **Fix**: Not applicable — this is the documented boundary between the
  deterministic and judgment layers (ADR-007), not a bug to fix.
- **Regression prevention**: Documented in `SKILL.md` under "Known
  Limitations."

## L8: Judgment-layer evaluation is single-rater and self-authored

- **What failed**: N/A (methodology limitation, disclosed proactively).
- **Why**: The 8 evaluation fixtures, their ground-truth expected defects,
  and the actual review findings in
  `evaluations/adversarial-diff-reviewer/actual/` were all produced by this
  same session's agent. There was no independent author for the ground truth
  and no independent reviewer performing the actual review.
- **Impact**: A 100% precision/recall result on these fixtures is much weaker
  evidence than it looks — it demonstrates the workflow is *executable and
  internally consistent*, not that it would perform this well on defects it
  didn't design the test around, or under an independent reviewer with no
  visibility into the intended answer. This is a stronger caveat than plain
  "single-rater" bias.
- **Fix**: Not fixable within one agent session. Requires either a second,
  independent agent/session reviewing the same fixtures blind, or real
  external usage (see [[16-assumptions-and-validation]] A5).
- **Regression prevention**: Stated explicitly in `RESULTS.md`'s summary,
  `SKILL.md`'s Evaluation section, and the Phase 2 completion report — never
  cite these scores as evidence of real-world review quality.

## L9: No runtime execution or test running

- **What failed**: N/A (scope boundary, not a bug).
- **Why**: The engine only parses diff text; neither it nor the SKILL.md
  workflow executes the changed code or runs a test suite.
- **Impact**: Cannot catch defects that only manifest at runtime (e.g. a type
  error only hit on a rare input path) unless they're also visible from
  reading the diff.
- **Fix**: Out of scope for this skill — a future skill (e.g. a future
  Acceptance Test Engineer, Phase 3) could compose with this one rather than
  this skill absorbing that scope.
- **Regression prevention**: Documented in `SKILL.md` under "When NOT to Use"
  and "Failure Conditions."

---

Entries below are from Phase 3 (acceptance-test-engineer).

## L10: `adversarial-diff-reviewer`'s CLI had zero test coverage (FIXED during Phase 3)

- **What failed**: `skills/adversarial-diff-reviewer/engine/cli.py` — stdin
  reading, `--out` directory writing, and the nonexistent-path exit-1 path —
  had no test exercising `main()` at all across the skill's 5 existing test
  files (19 tests, all against the engine modules directly).
- **Why**: Phase 2's test suite was written module-by-module against the
  engine internals; the CLI wrapper was assumed "thin enough not to need
  tests" and never revisited.
- **Impact**: Found by dogfooding `acceptance-test-engineer` against the
  CLI's real, already-shipped behavior (not a synthetic requirement) —
  see `examples/acceptance-test-engineer/example-run.md`. This is a gap in
  a *previous* phase's skill, surfaced by the *new* phase's skill — the
  first cross-skill dogfood finding in this project.
- **Fix**: `skills/adversarial-diff-reviewer/tests/test_cli.py` added (4
  tests) directly from the derived acceptance cases.
- **Regression prevention**: the new test file itself; suite is now 23/23.

## L11: Testability anti-pattern list is not exhaustive

- **What failed**: N/A (scope boundary, not a bug).
- **Why**: `patterns.py` is a fixed regex table (vague terms, weak modal
  verbs, two whole-document absence checks) — it can only match wording
  shapes it was written to recognize.
- **Impact**: Will over-flag (e.g. "should" used in a deliberate,
  RFC-2119-style non-mandatory clause is not actually a defect) and
  under-flag (any ambiguity that doesn't happen to use a known vague
  adjective or weak modal — most genuine scope ambiguity, like case-08's
  sentence-level contradiction, is invisible to this layer and only caught
  by the agent's Step 3 reasoning, exactly mirroring L7's role for the diff
  reviewer).
- **Fix**: Not applicable — documented boundary between the deterministic
  and judgment layers (ADR-007, reused for this skill).
- **Regression prevention**: Documented in `SKILL.md` under "Known
  Limitations."

## L12: No executable test code is generated — Gherkin text only

- **What failed**: N/A (deliberate scope decision, not a bug).
- **Why**: The skill has not read the real implementation being tested, so
  generating pytest/step-definition code would fabricate false precision
  about a system's actual API — it would look executable while being
  invented.
- **Impact**: The Acceptance Test Report's Gherkin block still requires a
  human or a separate, implementation-aware step to wire up real step
  definitions before it can run as an executable test suite.
- **Fix**: Not planned unless a future skill is explicitly scoped to compose
  this skill's output with real implementation knowledge (e.g. a future
  skill that reads the actual API via `codebase-intelligence` and generates
  glue code) — not this skill absorbing that scope.
- **Regression prevention**: Documented in `SKILL.md` under "When NOT to
  Use" and "Workflow" Step 4.

---

Entries below are from Phase 4 (feature-planner).

## L13: `acceptance-test-engineer`'s CLI had zero test coverage (FIXED during Phase 4)

- **What failed**: `skills/acceptance-test-engineer/engine/cli.py` — stdin
  reading, `--out` directory writing, and the nonexistent-path exit-1
  path — had no test exercising `main()` across any of its 5 existing test
  files (20 tests, all against the engine modules directly). Same gap shape
  as L10, in a different skill.
- **Why**: Same root cause as L10 — the CLI wrapper was assumed thin enough
  not to need dedicated tests and never revisited once the engine-module
  tests were in place.
- **Impact**: Found by dogfooding `feature-planner` against a real task
  targeting this exact CLI — see `examples/feature-planner/example-run.md`.
  The gap surfaced purely as a side effect of grounding "affected files" in
  the real module list, not from deliberately auditing test coverage. This
  is the second cross-skill dogfood finding in this project (after L10),
  and the first time a *planning* skill (rather than a review/testability
  skill) found one.
- **Fix**: `skills/acceptance-test-engineer/tests/test_cli.py` added (4
  tests, mirroring the L10 fix exactly). Suite is now 24/24.
- **Regression prevention**: the new test file itself.

## L14: Relevance scorer's path-weighting floods when task keywords collide with a shared directory name

- **What failed**: N/A (documented limitation, not a bug — found via real
  dogfooding, not fixed).
- **Why**: `relevance_scorer.py` weights a path match at 3 points per
  matched keyword. When a task's keywords happen to also be words in a
  shared parent directory name (e.g. "acceptance", "test", "engineer" in
  `skills/acceptance-test-engineer/`), *every* module under that directory
  gets the same path-weight bonus regardless of whether it's the file
  actually relevant to the task.
- **Impact**: In the real dogfood run
  (`examples/feature-planner/example-run.md`), the true target file
  (`skills/acceptance-test-engineer/engine/cli.py`) scored 13 and ranked
  13th of 65 — well below several test files and even an unrelated skill's
  file that scored higher purely from shared path vocabulary. The
  deterministic ranking alone would have pointed at the wrong file.
- **Fix**: Not fixed — this is the documented boundary between the
  deterministic layer (a lead generator) and the agent's Step 3 judgment
  (ADR-007), the same role L7/L11 play for the other two judgment-based
  skills. In the same dogfood run, the agent's judgment correctly
  identified `engine/cli.py` as the actual target despite its rank — real
  evidence the two-layer split does what it's designed to do, not just a
  theoretical justification for leaving this unfixed.
- **Regression prevention**: `SKILL.md`'s "Agent Responsibilities" section
  states explicitly: "a nonzero relevance score is not automatically
  in-scope either."

## L15: Planning anti-pattern list is not exhaustive

- **What failed**: N/A (scope boundary, not a bug).
- **Why**: `planning_patterns.py` is a fixed regex table (vague-scope
  terms, weak goal modals, two whole-text absence checks) — it can only
  match wording shapes it was written to recognize, same shape as L7/L11.
- **Impact**: Will over-flag (e.g. "improve" used with an already-precise
  follow-up clause) and under-flag (case-08's sentence-level scope
  contradiction is invisible to this layer — "only" alone satisfies the
  scope-boundary absence check even though the next sentence directly
  contradicts it — and is only caught by the agent's Step 3 reasoning).
- **Fix**: Not applicable — documented boundary between the deterministic
  and judgment layers (ADR-007, reused for this skill).
- **Regression prevention**: Documented in `SKILL.md` under "Known
  Limitations."
