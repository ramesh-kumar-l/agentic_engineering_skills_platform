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

## L16: Action-classifier used a fixed-distance proximity window, which real phrasing exceeded (FIXED during Phase 5)

- **What failed**: `action_patterns.py`'s verb+object categories (e.g.
  "push ... origin" for Publishing) originally required both terms to
  appear within a fixed character-distance window of each other in a single
  regex. The window was tuned against short synthetic phrasing.
- **Why**: A real dogfood run's action description ("Commit and push the
  new Security Context Guard skill files (skills/security-context-guard/,
  evaluations/security-context-guard/, project-memory-bank updates) to the
  shared origin repository.") put a parenthetical object list between the
  verb and its target — over 150 characters apart. Widening the window from
  20 to 80 characters (the first fix attempt) still wasn't enough, and no
  fixed window is well-justified for free-text phrasing in general.
- **Impact**: Found via dogfooding `security-context-guard` against its own
  real source and a real pending git-push decision this session actually
  faced — see `examples/security-context-guard/example-run.md`. The first
  run produced `AUTHORIZE` with zero action-category matches for an action
  that should have been flagged `Publishing` — a real false negative on
  exactly the kind of decision this skill exists to catch, caught before it
  could mislead anyone only because the dogfood run was against real
  phrasing, not a synthetic fixture. This is the third instance of "a real
  dogfood run on real phrasing found a gap a synthetic fixture didn't"
  (after L1 and L13), and the first where the gap was in the very skill
  being dogfooded rather than a different one.
- **Fix**: Replaced the fixed-distance window with same-sentence
  co-occurrence matching — `ActionPattern.matches()` in `action_patterns.py`
  splits the action text into sentences and checks whether the verb pattern
  and the object pattern each appear somewhere in the same sentence,
  regardless of distance. A better-justified design (matches how the
  ambiguity in real phrasing actually works), not just a bigger magic
  number.
- **Regression prevention**:
  `tests/test_action_patterns.py::test_publishing_matches_with_an_object_list_between_verb_and_target`
  (the exact real sentence that exposed the gap) plus a paired negative
  test, `test_publishing_does_not_match_push_in_an_unrelated_later_sentence`,
  confirming same-sentence matching doesn't just degrade into "matches
  anywhere in the whole text."

## L17: Secret/PII/action pattern tables are heuristic, leads-not-verdicts, and not exhaustive

- **What failed**: N/A (scope boundary, not a bug — same shape as
  L3/L7/L11/L15).
- **Why**: `secret_patterns.py`, `pii_patterns.py`, and `action_patterns.py`
  are fixed regex tables. They can only match shapes they were written to
  recognize (e.g. a handful of common secret/PII/action-verb shapes), will
  miss secrets/PII in formats not covered (e.g. a cloud provider's specific
  key format not in the table), and can false-positive (e.g. a
  13-16-digit run that isn't actually a credit card number).
- **Impact**: `SKILL.md`'s "When NOT to Use" section states this explicitly
  — this skill's output is never proof content contains no sensitive data,
  only a lead-generating pass. The agent's Step 3 judgment and, ultimately,
  a human's own review remain necessary for anything genuinely
  high-stakes.
- **Fix**: Not applicable — documented boundary between the deterministic
  layer (a lead generator, same role as every other Pattern 2 skill's
  fixed table) and human judgment, which for a *security* classification
  skill sits partly with the agent's Step 3 reasoning and partly with the
  human approver (ADR-011).
- **Regression prevention**: Documented in `SKILL.md` under "When NOT to
  Use" and "Known Limitations."

## L8 update: now applying a fourth time

`security-context-guard`'s judgment-layer evaluation also scored 100%
precision/recall against self-authored ground truth
(`evaluations/security-context-guard/RESULTS.md`) — four-for-four across
every judgment-based skill built so far. Same standing caveat as Phases
2-4: this continues to show the evaluation design cannot yet discriminate a
genuinely good derivation from a mediocre one, not that any of the four
skills performs well in the world. See [[16-assumptions-and-validation]] A5.

## L18: Symptom anti-pattern list and stack-trace parser are not exhaustive

- **What failed**: N/A (scope boundary, not a bug — same shape as
  L3/L7/L11/L15/L17).
- **Why**: `symptom_patterns.py` is a small fixed regex table (2 wording
  patterns + 3 absence checks); `stack_trace_parser.py` covers exactly two
  shapes (Python tracebacks, generic `path:line`). A symptom written in
  other phrasing, or a stack trace from a language/runtime whose format
  differs (e.g. JavaScript's `at func (file:line:col)`, Java's
  `at pkg.Class.method(File.java:42)`), will not be recognized.
- **Impact**: `SKILL.md`'s Known Limitations section states this
  explicitly. A missed stack-trace shape silently falls back to
  keyword-tier scoring only — not a hard failure, but a real, disclosed
  precision loss for non-Python stack traces specifically.
- **Fix**: Not applicable — documented boundary between the deterministic
  layer (a lead generator, same role as every other Pattern 2 skill's fixed
  table) and the agent's own judgment, which can recognize an unfamiliar
  trace shape by reading it directly even when the regex table can't.
- **Regression prevention**: Documented in `SKILL.md` under "Known
  Limitations."

## L19: Keyword-tier candidate scoring shares feature-planner's coincidental-substring limitation, and produced this project's first non-perfect judgment-layer score

- **What failed**: N/A (inherited limitation, not a new bug — same
  mechanism as L14).
- **Why**: `candidate_scorer.py`'s keyword-tier matching is substring-based,
  same as `feature-planner/engine/relevance_scorer.py` (ADR-010's
  precedent). Evaluation case-03 (`evaluations/root-cause-analyzer/fixtures/
  case-03-vague-report/`) demonstrated this directly: the word "work" in
  "doesn't work" matched `engine/worker.py` purely as a substring, and
  "app" in "The app is just broken" matched `engine/app.py` — both
  coincidental, not real evidence of involvement.
- **Impact**: this is the first evaluation case, across five judgment-based
  skills, where the agent's actual derivation scored below perfect
  precision/recall against hand-authored expected categories (0.67/0.67 —
  `evaluations/root-cause-analyzer/RESULTS.md`, case-03). This was not
  adjusted to look better; the expected-category keywords for that case
  were written before the actual derivation and left as originally
  authored. It breaks the "four-for-four perfect scores" pattern noted in
  the L8 updates above — read as a data point that this evaluation design
  *can* produce imperfect scores when the expected/actual wording
  genuinely diverges, not as evidence this skill's judgment quality is
  lower than the other four's (a single self-authored case cannot support
  either claim). See [[16-assumptions-and-validation]] A5.
- **Fix**: Not applicable — the deterministic layer working as designed
  (surfacing a lead, not a verdict) is exactly why case-03's actual
  derivation explicitly states both matches are coincidental rather than
  presenting them as real candidates (see `evaluations/root-cause-analyzer/
  actual/case-03-vague-report.actual.json`).
- **Regression prevention**: `evaluations/root-cause-analyzer/eval_cases/
  case-03-vague-report.md` documents the expected failure mode explicitly
  (false confidence on a coincidental match) as the thing being tested for.

## L8 update: now applying a fifth time, first non-perfect score

`root-cause-analyzer`'s judgment-layer evaluation scored perfect
precision/recall on 7 of 8 fixtures and 0.67/0.67 on the 8th (case-03) —
see L19 above and `evaluations/root-cause-analyzer/RESULTS.md`. This is the
fifth judgment-based skill evaluated this way, and the first whose score is
not a clean 100% — still self-authored, single-rater evidence either way,
so neither outcome should be read as proof of real-world diagnostic
quality. See [[16-assumptions-and-validation]] A5.

## L20: Tradeoff-detection regex missed the verb form "trades X for Y" (FIXED same-session, found via real dogfooding)

- **What failed**: `decision_patterns.py`'s `no-tradeoff-signal` absence
  pattern matched only the noun forms `tradeoff`/`trade-off` (plus
  cost/downside/risk/however/but/at-the-expense-of), not the verb phrasing
  "Option A trades X for Y" — a natural, common way to state a tradeoff in
  English that the initial pattern table did not anticipate.
- **Why**: found via the real dogfood run
  (`examples/architecture-decision/example-run.md`), not a synthetic
  fixture — the dogfood decision text used "trades flexibility ... for
  correctness" and "trades correctness for reach" to state two real
  tradeoffs, and the first engine run still flagged `no-tradeoff-signal` as
  if neither had been stated. Same pattern as L16 (`security-context-guard`):
  a regex table validated only against hand-authored synthetic fixtures
  missed a real phrasing the first genuine, real-text use of the tool hit
  immediately.
- **Impact**: a false absence-flag on a decision that actually did state
  its tradeoffs — the kind of false-negative-on-the-flag-itself error that
  erodes trust in the anti-pattern table if left uncorrected, since the
  whole point of the flag is to catch decisions that genuinely omit this.
- **Fix**: added `trades?\b` to the tradeoff regex alternation in
  `engine/decision_patterns.py`. Re-verified: all 34 unit/integration/CLI
  tests still pass, all 8 evaluation fixtures still score correctly (none
  of the synthetic fixtures relied on the verb form being *absent* to
  trigger the flag), and the dogfood decision's `no-tradeoff-signal` flag
  no longer fires after the fix.
- **Regression prevention**: `tests/test_decision_scanner.py` covers the
  noun-form and absence cases; the dogfood write-up in
  `examples/architecture-decision/example-run.md` documents the verb-form
  gap explicitly as the thing that was found and fixed, so a future
  regression is at least documented context even though no fixture
  currently pins the verb-form case directly (a gap worth closing if this
  skill sees more real use).

## L21: Blast-radius keyword scoring degrades sharply at full-repository scale when a decision is about the platform's own architecture

- **What failed**: N/A (disclosed limitation, not fixed — same mechanism
  class as L14 and L19, demonstrated more sharply here).
- **Why**: `impact_scorer.py`'s keyword matching is substring-based and has
  no stopword for common path-prefix tokens (e.g. `engine`, which every
  module in this repo's `skills/*/engine/` layout shares). Evaluation
  case-01 and case-05 already demonstrated this at small scale (2-3 module
  fixtures). The real dogfood run
  (`examples/architecture-decision/example-run.md`) demonstrated it far
  more sharply: a decision *about the architecture-decision skill's own
  required-composition choice* — necessarily written using this project's
  own recurring vocabulary ("codebase", "intelligence", "report", "adr",
  "composition", "decision") — produced a blast-radius score of 241–256 and
  matched all 10 of the report's hotspots for *both* options, against a
  143-module, 7-skill repository whose own documentation constantly reuses
  exactly that vocabulary.
- **Impact**: at this scale, the blast-radius signal is real (every listed
  module genuinely contains the matched words) but not useful — it cannot
  distinguish "this decision is about the whole platform" from "this
  decision's wording happens to overlap this repo's own vocabulary
  everywhere." A keyword-only scorer cannot fix this on its own.
- **Fix**: Not applied. A real fix would need either TF-IDF-style
  down-weighting of corpus-common terms or a minimum keyword-specificity
  threshold, neither implemented — this tradeoff (added complexity vs. a
  disclosed, understood limitation, ADR-013's Future Evolution clause) has
  not been evaluated against real evidence of need beyond this single
  dogfood run.
- **Regression prevention**: `examples/architecture-decision/example-run.md`
  documents this explicitly as a limitation observed on real use, not
  papered over; `SKILL.md`'s "When NOT to Use" section warns against
  trusting this skill's blast-radius signal for a decision about the
  platform's own architecture at large.

## L8 update: now applying a sixth time, back to perfect scores

`architecture-decision`'s judgment-layer evaluation scored perfect
precision/recall on all 8 fixtures — unlike `root-cause-analyzer`'s Phase 6
(one non-perfect case, L19 above). This is the sixth judgment-based skill
evaluated this way; still self-authored, single-rater evidence, so this
should not be read as evidence this skill's judgment quality is higher than
`root-cause-analyzer`'s — a single self-authored evaluation cannot support
that comparison either way. See [[16-assumptions-and-validation]] A5.

## L22: `codebase-intelligence`'s `fan_in` can undercount a real caller relative to `refactoring-safety`'s own caller scan

- **What**: `refactoring-safety`'s real dogfood run
  (`examples/refactoring-safety/example-run.md`) assessed a genuine refactor
  target (`skills/refactoring-safety/engine/target_resolver.py`) whose
  Markdown output listed **two** real callers via the engine's own
  `caller_modules` scan (`engine/report.py`, a relative-import caller, and
  `tests/test_target_resolver.py`, an absolute-style-import caller) — but
  `codebase-intelligence`'s own `dependency_graph.fan_in` for that same
  module reported **1**, not 2.
- **Why**: `codebase-intelligence`'s dependency-graph builder only
  constructed a `DependencyEdge` for the relative import
  (`.target_resolver`); the test file's absolute-style import
  (`engine.target_resolver`) was a real caller but was not recognized as an
  edge into that same graph. `refactoring-safety`'s `target_resolver.py`
  does not trust `fan_in` for caller *identity* — its `_find_callers`
  independently scans every module's raw `imports` list by substring, so it
  found both callers correctly — but `safety_scorer.py`'s risk-tier
  calculation scores against the authoritative `fan_in` number (1), not the
  length of `caller_modules` (2), for consistency with `codebase-
  intelligence`'s own reported metric.
- **Impact**: in the dogfood case this did not change the outcome (an
  `extract` operation on a non-hotspot module stays `low` risk either way),
  but on a **boundary-changing** operation (rename/delete/move/change-
  signature) where the fan-in threshold sits at the boundary between tiers,
  this gap could under-score a target's real risk by one real caller.
- **Fix**: Not applied. This gap originates in `codebase-intelligence`'s
  own dependency-graph construction, not in `refactoring-safety`'s code —
  fixing it here would mean either trusting `caller_modules`' length over
  `codebase-intelligence`'s own `fan_in` field (a real design tradeoff not
  evaluated against other evidence yet) or fixing the upstream graph
  builder to recognize absolute-style cross-package imports as edges (a
  different skill's concern). See ADR-014's Future Evolution clause.
- **Regression prevention**: `examples/refactoring-safety/example-run.md`
  documents this explicitly as a limitation observed on real use;
  `SKILL.md`'s "When NOT to Use" and Agent Responsibilities sections
  instruct the agent to check `caller_modules` directly rather than
  trusting `fan_in` alone as the complete caller picture.

## L8 update: now applying a seventh time, still perfect scores

`refactoring-safety`'s judgment-layer evaluation scored perfect precision/
recall on all 8 fixtures, same as five of the six prior judgment-based
skills — `root-cause-analyzer` remains the one exception (L19 above). This
is the seventh judgment-based skill evaluated this way; still self-authored,
single-rater evidence, so this should not be read as evidence this skill's
judgment quality is higher than `root-cause-analyzer`'s — a single
self-authored evaluation cannot support that comparison either way. See
[[16-assumptions-and-validation]] A5.

---

Entries below are from Phase 9 (regression-hunter).

## L23: `target_resolver.py`'s substring-based caller identification produces a wildly inflated caller list for short, common module stems (FIXED 2026-08-26, mentor-review follow-up)

- **What failed**: N/A (disclosed limitation, not fixed — same mechanism
  class as L14/L19/L21, demonstrated in a new location: structural caller
  identification, not keyword-relevance ranking).
- **Why**: `regression-hunter`'s `target_resolver.py::_find_callers` (an
  independent copy of `refactoring-safety`'s identical
  `target_resolver.py::_find_callers` pattern) resolves a changed file's
  module stem, then checks whether that stem appears as a bare **substring**
  anywhere in each candidate module's joined `imports` text
  (`target_stem in imports_text`). For `codebase-intelligence/engine/
  scanner.py`, the stem `"scanner"` is a substring of `"testability_
  scanner"`, `"decision_scanner"`, `"safety_scanner"`, `"regression_
  scanner"`, `"symptom_scanner"`, and `"risk_scanner"` — every other skill
  in this platform that reuses Pattern 2's "scanner" naming convention for
  its own anti-pattern-flag module.
- **Impact**: found via the real dogfood run
  (`examples/regression-hunter/example-run.md`) — a genuine, already-tested
  `codebase-intelligence` scanner fix (excluding `*.egg-info` directories
  from repo scans). The Markdown output listed **22 "caller" modules** for
  `scanner.py`, most of them false positives — modules like
  `skills/architecture-decision/engine/report.py` that import their own
  skill's `decision_scanner.py` and have never heard of `codebase-
  intelligence/engine/scanner.py` at all. In this specific run the false
  positives did not change `overall_risk_tier` (which is driven by the
  composed report's real `fan_in`/hotspot data, not by the length of
  `caller_modules`), but the `caller_modules` list itself — which
  `SKILL.md`'s Agent Responsibilities explicitly instructs the agent to
  check alongside `fan_in` — is materially misleading for any module whose
  stem is a short, common word. This is also the first time this class of
  limitation is shown to affect **two** skills' independent copies of the
  same heuristic simultaneously (`refactoring-safety`'s and
  `regression-hunter`'s `target_resolver.py` share the identical
  vulnerability, since the second is a portability-discipline-driven
  independent copy of the first's resolution pattern, not a shared import).
- **Fix**: Applied 2026-08-26, after a mentor-review pass explicitly
  flagged this as having crossed from "disclosed tradeoff" to "proven,
  four-times-recurring correctness bug" once L24 showed the same heuristic
  could corrupt a decision signal, not just a displayed field. Both
  `refactoring-safety/engine/target_resolver.py` and
  `regression-hunter/engine/target_resolver.py` now use a word-boundary-
  aware match (`_contains_whole_token`, `re.search(r"\b<stem>\b", ...)`)
  instead of a bare `in` substring check. Since `\w` includes `_`,
  `\bscanner\b` correctly rejects "testability_scanner" (no boundary
  between `_` and `s`) while still matching a real, dotted import like
  "engine.scanner" (boundary at `.`) — exactly the collision this entry
  documented. Applied identically (independent copy, no shared import,
  same portability discipline as the original bug) to both skills.
- **Regression prevention**: `test_caller_list_excludes_module_whose_
  import_merely_embeds_the_stem_substring`-shaped tests added to both
  skills' `tests/test_target_resolver.py`, using the exact
  `scanner`/`testability_scanner` collision from this entry's dogfood
  finding, paired with a positive-case test confirming a real dotted
  import still resolves correctly. `examples/regression-hunter/
  example-run.md` remains as historical record of the original finding.

## L8 update: now applying an eighth time, still perfect scores

`regression-hunter`'s judgment-layer evaluation scored perfect precision/
recall on all 8 fixtures, same as six of the seven prior judgment-based
skills — `root-cause-analyzer` remains the one exception (L19 above). This
is the eighth judgment-based skill evaluated this way; still self-authored,
single-rater evidence, so this should not be read as evidence this skill's
judgment quality is higher than `root-cause-analyzer`'s — a single
self-authored evaluation cannot support that comparison either way. See
[[16-assumptions-and-validation]] A5.

---

Entries below are from Phase 10 (release-readiness).

## L24: `target_resolver.py`'s substring-based resolution produces false-positive TEST COVERAGE, not just an inflated caller list — a materially new manifestation of L23

- **What failed**: N/A (disclosed limitation, not fixed — same mechanism
  class as L14/L19/L21/L23, demonstrated in a new, more consequential
  location: false-positive test-coverage matching, not just caller-list
  inflation).
- **Why**: `release-readiness`'s `target_resolver.py` is a THIRD
  independent copy of `refactoring-safety`'s/`regression-hunter`'s
  identical stem-based substring-matching pattern (already disclosed as
  L23). `test_coverage_scanner.py` reuses the exact same substring check
  (`target_stem in imports_text`) to decide whether a "looks like a test"
  module genuinely covers a given file. For a module whose stem is a
  common word shared across this platform's skills (e.g. `models`,
  `stats`, `report`, `render_json`, `render_markdown`, `ci_report_loader`,
  `target_resolver`, `test_coverage_scanner` — every module reusing Pattern
  2's common naming convention for these roles), this produces a
  false-positive "covered" verdict: a test module belonging to a
  completely unrelated skill, which merely imports its OWN skill's
  identically-stemmed module, is counted as covering this skill's module.
- **Impact**: found via the real dogfood run
  (`examples/release-readiness/example-run.md`) — `skills/release-
  readiness/engine/models.py` resolved with `fan_in: 13` (structural tier
  `high`) and `test_coverage.has_coverage: true`, "covered" by
  `skills/architecture-decision/tests/test_impact_scorer.py` and
  `skills/architecture-decision/tests/test_stats.py`, among others — but
  `release-readiness` has **no `tests/test_models.py` of its own**. The
  same false-positive pattern repeated for `stats.py`, `report.py`,
  `render_json.py`, `render_markdown.py`, `ci_report_loader.py`,
  `target_resolver.py`, and `test_coverage_scanner.py`. This is a more
  consequential category of finding than L23: L23 (found via
  `regression-hunter`'s dogfood run) inflated a *caller list* — a
  displayed field that did not change that run's risk-tier outcome. Here,
  the identical heuristic corrupts the exact signal
  (`test_coverage.has_coverage`) `readiness_scorer.py`'s rule table uses to
  decide whether a structurally consequential file needs closer review —
  the mechanism is now shown capable of making a genuinely untested new
  module look tested, the more dangerous direction for a skill whose
  entire purpose is judging release readiness. In this specific dogfood
  run the outcome still landed conservatively (`needs-review`, not
  `clear`), because the same collision also inflated `fan_in`/hotspot
  status enough to keep the structural tier at medium/high — but that is
  a coincidence of this run's specific module names, not a property of the
  fix.
- **Fix**: PARTIALLY applied 2026-08-26. Both `target_resolver.py` and
  `test_coverage_scanner.py` in `release-readiness` now use the same
  word-boundary-aware match introduced for L23
  (`_contains_whole_token`, `re.search(r"\b<stem>\b", ...)`) instead of a
  bare substring check. This closes the *embedded-substring* subclass of
  this bug (a stem like "models" appearing inside an unrelated identifier
  such as "shared_models_cache") for both caller identification and test
  coverage matching. **It does NOT close this entry's headline dogfood
  example**: two different skills each having their own genuinely,
  legitimately-imported, identically-stemmed module (e.g.
  `architecture-decision`'s `models.py` and `release-readiness`'s own
  `models.py`) still produces a real, boundary-respecting dotted-import
  match — `\bmodels\b` matches "engine.models" regardless of *which*
  skill's `engine/models.py` it actually refers to, because the resolver
  has no notion of "same skill" scoping. Closing that remaining gap
  requires a repo-layout-aware fix (e.g. scoping matches to the same
  `skills/<name>/` path prefix as the resolved target) that was
  deliberately NOT implemented in this pass — it is a larger, more
  repo-layout-specific change than the general-purpose word-boundary fix,
  and risks introducing false negatives for genuinely cross-directory
  callers in a non-monorepo target repo, not evaluated against evidence of
  need. This entry stays open, narrowed to exactly this remaining scope.
- **Regression prevention**: `test_excludes_test_module_whose_import_
  merely_embeds_the_stem_substring` and a paired positive-case test added
  to `release-readiness`'s `tests/test_target_resolver.py` and
  `tests/test_test_coverage_scanner.py`, confirming the embedded-substring
  subclass is closed while a real dotted-import match still resolves
  correctly. `examples/release-readiness/example-run.md` remains the
  historical record of the original, still-partially-open finding.
  `SKILL.md`'s Known Limitations section should be read alongside this
  updated entry — the cross-skill identical-stem gap is real and current,
  not historical.

## L8 update: now applying a ninth time, still perfect scores

`release-readiness`'s judgment-layer evaluation scored perfect precision/
recall on all 8 fixtures, same as seven of the eight prior judgment-based
skills — `root-cause-analyzer` remains the one exception (L19 above). This
is the ninth judgment-based skill evaluated this way; still self-authored,
single-rater evidence, so this should not be read as evidence this skill's
judgment quality is higher than `root-cause-analyzer`'s — a single
self-authored evaluation cannot support that comparison either way. See
[[16-assumptions-and-validation]] A5.

## L25: `dependency-supply-chain` has no live CVE/vulnerability-database lookup

**Status**: Scope decision, not a bug — disclosed upfront in `SKILL.md`'s
When NOT to Use and Known Limitations sections, not discovered later.

This project makes no network calls (ADR-006, stdlib-only, offline). A
"supply-chain" skill without a live vulnerability feed cannot tell a user
that a specific installed version is actually exploitable — it can only
check offline-derivable signal (pin status, a small curated known-risk-name
table, duplicate/conflicting version declarations, surface area). Use a
real SCA tool (`pip-audit`, `npm audit`, Dependabot, Snyk, etc.) alongside
this skill for real vulnerability data.

**Regression prevention**: N/A — this is a permanent scope boundary, not a
defect to regress on. `risk_patterns.py`'s known-risk table is explicitly
five entries, each citing a real public incident, not a substitute for a
CVE feed.

## L26: `dependency-supply-chain` has no per-dependency license-risk detection

**Status**: Scope decision, corrected during implementation (not shipped
then found broken) — the original Phase 11 plan included a
`license_patterns.py` module; it was dropped before merging, once it became
clear the data it would need doesn't exist in what's available.

A manifest's own `license` field (`package.json`, `pyproject.toml`)
describes the *project's* declared license, not each individual
dependency's license — that data isn't captured by
`codebase-intelligence`'s `external_deps.py` at all. Getting real
per-dependency license data would require inspecting installed package
metadata (`site-packages`/`node_modules`), which isn't guaranteed to exist
at scan time and would make this skill's output depend on the target
environment's install state rather than its declared manifests alone.
Shipping a "license risk" flag from data that doesn't exist would have been
exactly the kind of ungrounded, plausible-looking output ADR-010 exists to
prevent — see ADR-017.

**Regression prevention**: `SKILL.md`'s Dependency Risk Checklist item 4
requires the agent to state "not available" explicitly every walk, rather
than silently omitting the category — `evaluations/dependency-supply-chain/`
's `run_evaluation.py` docstring and `RESULTS.md` both restate this caveat.
Real per-dependency license detection is named as a future-evolution item
in ADR-017, to be built only against real evidence of need.
