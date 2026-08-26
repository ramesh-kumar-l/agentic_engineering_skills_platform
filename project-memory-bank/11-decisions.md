# 11 — Architectural Decisions

Append-only log. Each entry runs through the decision checklist: User Value,
Correctness, Security, Simplicity, Maintainability, Portability, Evidence,
Future Evolution (do not solve hypothetical future problems prematurely).

---

## ADR-001: Adopt the operating charter as the project's governing model

**Decision**: Follow the full operating charter (vision, thesis, phase roadmap,
skill contract, evaluation framework, security model, sprint model,
token-efficiency protocol) as the governing process for this project.

- User Value: forces every phase to justify itself against real engineer
  outcomes (Time-to-Correct-Result) instead of feature count.
- Correctness: mandates evaluation cases and layered review before trust claims.
- Security: mandates classify→minimize→sanitize→authorize→execute→audit and
  human checkpoints for high-risk actions from day one.
- Simplicity: explicitly forbids building all 15 skills or a platform/UI before
  3 skills are proven.
- Maintainability: memory bank ([[07-current-state]] etc.) replaces re-deriving
  context each session.
- Portability: `SKILL.md` is declared the *initial*, not final, representation.
- Evidence: mandates an assumptions ledger ([[16-assumptions-and-validation]])
  that can invalidate the roadmap.
- Future Evolution: phase-by-phase STOP gates preserve the option to change
  direction at every boundary.

**Status**: Adopted.

**Addendum (2026-08-26)**: the operating charter this ADR adopts was, until
today, referenced by name but never checked into the repo. It is now filed
at [[operating-charter]], confirmed complete by the user. That version
contains Sections 1–11 only; this file's own citations and others'
(Section 39–40, Section 43, "First Activation") point past that range —
see [[12-known-limitations|L27]] for the disclosed discrepancy.

---

## ADR-002: `SKILL.md` is the initial portable representation, not a permanent one

**Decision**: Treat "Skill" as the durable conceptual abstraction and `SKILL.md`
(Markdown) as the first concrete, portable representation of it. The system must
remain able to migrate to a different representation later if evidence shows
one serves better (e.g., a structured/typed format for tooling, or a different
format for a specific runtime).

- Evidence: none yet either way — Markdown chosen for today's cross-runtime
  readability and human-editability, not because it's proven optimal.
- Future Evolution: do not hard-couple evaluation harness, registry, or UI
  designs to Markdown parsing in a way that would block a future format change.

**Status**: Adopted.

---

## ADR-003: Defer all skill implementation to Phase 1+

**Decision**: Phase 0 produces documentation only (memory bank, contract,
frameworks). No `skills/`, `workflows/`, `evaluations/`, `examples/`, or `docs/`
directories are created yet — they appear when Phase 1 has real content for
them.

- Simplicity: avoids empty placeholder directories with no content.
- Evidence: nothing to evaluate yet; premature scaffolding would be unvalidated
  structure.

**Status**: Adopted.

---

## ADR-004: First-five skill validation order

**Decision**: Codebase Intelligence → Adversarial Diff Reviewer →
Acceptance Test Engineer → Feature Planner → Security Context Guard (see
[[08-roadmap]] for full rationale).

- User Value: understand → verify → define-correctness maps directly onto how
  engineers actually approach unfamiliar changes.
- Correctness: each of the first three skills is independently testable against
  real diffs/repos without needing orchestration to exist first.
- Simplicity: no composition/workflow machinery required to validate any of the
  first three.
- Future Evolution: Feature Planner (plan-then-implement) is deferred until
  understand/verify/define-correctness are validated, so planning work is
  informed by real evidence rather than assumption.

**Status**: Adopted, pending Phase 1 execution and re-validation at each phase
boundary per [[08-roadmap]]'s adaptive-roadmap rule.

---

## ADR-005: SKILL.md + deterministic engine hybrid pattern

**Decision**: A skill's contract (`SKILL.md`) may wrap a small, deterministic,
stdlib-only backing tool rather than relying purely on LLM reasoning via the
agent's own tools, when the underlying task is deterministic/repeatable
(structure extraction, parsing, graph-building) rather than a judgment call.
Established via `codebase-intelligence` ([[03-architecture]]).

- User Value: deterministic scans are cheaper, faster, and repeatable across
  runs than repeated ad hoc Grep/Read exploration by an agent.
- Correctness: deterministic code is unit-testable in a way LLM reasoning is
  not — 23 tests + 4 evaluation fixtures back this skill's structural claims.
- Security: the engine is read-only and never emits secret-shaped file
  contents (see [[06-security-model]]); verified by test.
- Simplicity: only used where the task is genuinely deterministic — judgment
  tasks (e.g. diff review) stay in the SKILL.md workflow, not baked into code.
- Maintainability: each engine module is single-responsibility, <300 lines.
- Portability: stdlib-only (ADR-006) keeps the engine runnable without a
  dependency install step, across any agent runtime with Bash + Python.
- Evidence: proven buildable and testable via the codebase-intelligence
  reference implementation; dogfooding caught a real bug pre-ship (L1 in
  [[12-known-limitations]]).
- Future Evolution: later skills (diff reviewer, feature planner, etc.) can
  adopt or skip this pattern per-skill based on whether their task is
  deterministic — this ADR does not mandate it universally.

**Status**: Adopted.

---

## ADR-006: codebase-intelligence engine is Python, stdlib-only

**Decision**: The engine has zero third-party runtime dependencies (only
`pytest` as a dev-only dependency for running tests).

- User Value: no install step beyond a Python 3.10+ interpreter — works in any
  agent's Bash environment without a package-manager round trip.
- Portability (NFR1 in [[02-requirements]]): avoids lock-in to a specific
  packaging ecosystem's dependency resolution behavior.
- Simplicity: `ast`, `os`, `pathlib`, `json`, `re`, `dataclasses` cover the
  full requirement; no dependency-management surface to maintain.
- Evidence: none yet that a third-party dependency would meaningfully improve
  results — chosen for today's simplicity, not proven optimal long-term.
- Future Evolution: if a future skill genuinely needs a real multi-language
  parser (e.g. tree-sitter) instead of heuristics (see [[12-known-limitations]]
  L3), that tradeoff should be evaluated then, against real evidence of need —
  not pre-adopted here.

**Status**: Adopted.

---

## ADR-007: Deterministic pre-processor + agent-driven adversarial workflow for judgment-based skills

**Decision**: For skills where the core task is a judgment call (defect
detection, review, risk assessment — not structure extraction), split the
work into two layers: a small stdlib-only deterministic engine that parses
input and flags mechanically-detectable patterns as *leads*, and an
agent-driven workflow (defined in `SKILL.md`) that performs the actual
adversarial reasoning against a fixed failure-first checklist. Established via
`adversarial-diff-reviewer` ([[03-architecture]]).

- User Value: catches both the mechanical cases cheaply (regex) and the
  judgment cases the engine cannot honestly claim to catch (subtle/
  concurrency/logic bugs) — see the dogfood example where the deterministic
  layer stayed silent but the agent found a real defect
  (`examples/adversarial-diff-reviewer/example-run.md`).
- Correctness: the deterministic layer is unit-tested (19 tests); the
  judgment layer is evaluated via 8 seeded-defect fixtures with the agent's
  actual findings scored against ground truth
  (`evaluations/adversarial-diff-reviewer/RESULTS.md`) — but see L8 in
  [[12-known-limitations]]: this evidence is single-rater and self-authored,
  not independently verified.
- Security: risk-flag patterns matched in added lines are never echoed
  unredacted into engine output (ADR-008); verified by test, and a real
  redaction gap was found and fixed twice during this phase (L5, L6 in
  [[12-known-limitations]]).
- Simplicity: this pattern is explicitly the counterpart to ADR-005, not a
  replacement — deterministic-only (ADR-005) stays the right choice for
  genuinely deterministic tasks; this pattern is for tasks where that would
  be dishonest.
- Maintainability: engine modules remain single-responsibility, <300 lines,
  independently testable from the workflow logic in `SKILL.md`.
- Portability: stdlib-only engine (same rationale as ADR-006).
- Evidence: proven buildable via the adversarial-diff-reviewer reference
  implementation; the real, in-session dogfood catch (L6) is the strongest
  evidence so far that the two-layer split adds value over either layer
  alone.
- Future Evolution: later judgment-based skills (feature planner, root-cause
  analyzer, etc.) can adopt this pattern; the specific failure-first checklist
  and risk-pattern table are per-skill, not generalized here ahead of
  evidence they should be shared.

**Status**: Adopted.

---

## ADR-008: Redact, not exclude, secrets found in diff content

**Decision**: Unlike `codebase-intelligence` (ADR-005), which never reads
secret-shaped *files* at all, `adversarial-diff-reviewer` must read diff
content that may contain a newly-added hardcoded secret — that is exactly one
of the defects it needs to catch. Instead of excluding such lines, the engine
redacts the matched secret span (`<redacted>`) in place, in both the risk flag
and the underlying line content, before any output is produced.

- User Value: the agent still sees that a secret-shaped literal was added
  (file/line/pattern-type) and can flag it as a finding, without the actual
  secret value propagating into a report artifact that might be logged,
  displayed, or pasted into a PR comment.
- Correctness: `pattern.regex.sub()` (not `search()` + slice) redacts every
  occurrence per line, not just the first (L6 in [[12-known-limitations]]).
- Security: directly implements [[06-security-model]]'s "never expose
  credentials/tokens/secrets" for a case Phase 1's "skip the whole file"
  approach cannot handle, since the file here (the diff) is the thing being
  reviewed, not incidental.
- Simplicity: one redaction mechanism, applied consistently to both output
  surfaces (flag and raw content) rather than two separate rules.
- Evidence: verified by
  `tests/test_integration.py::test_secret_value_never_leaks_into_json_or_markdown`
  and `tests/test_risk_scanner.py::test_all_occurrences_of_a_secret_pattern_on_one_line_are_redacted`.
- Future Evolution: if a future skill needs to reason about the *actual*
  secret value (not just its presence), that would need an explicit,
  separately-authorized secure mechanism — not assumed here.

**Status**: Adopted.

---

## ADR-009: Internal viability pilots must never be presented as the validated experiment

**Decision**: When a validation experiment ([[01-product-thesis]] Experiment
A/B/C) is not yet actually runnable (missing an independent party, a real
task, or a real measurement), it is acceptable to run a small, explicitly-
labeled internal pilot (single session, N=1, un-blinded, self-run) to sanity-
check direction — but the pilot's result must never be written up, cited, or
have the assumptions ledger status upgraded as if it were the real
experiment. Established in Phase 3 ([[17-experiment-viability-check]]),
generalizing the disclosure discipline already used for L8.

- User Value: keeps every claim in the repo honestly scoped, so future
  decisions (including whether to invest in Phase 14's Workflow Composer)
  aren't built on evidence that looks stronger than it is.
- Correctness: a pilot and an experiment answer different questions — "is
  this executable and does it show a plausible signal" vs. "is this actually
  better, measured against an independent baseline." Conflating them would
  corrupt the assumptions ledger's evidentiary value.
- Evidence: Pilot A and Pilot B in [[17-experiment-viability-check]] both
  found plausible signal (an assumption made explicit that direct reasoning
  skipped; a composition win on one requirement shape) — real observations,
  explicitly bounded as N=1 and non-generalizable.
- Simplicity: one clear rule ("pilot ≠ experiment, always label which one
  this is") rather than a graduated confidence scale that invites rounding
  up.
- Future Evolution: the actual Experiment A/B still require an independent
  party; this ADR does not change what's needed to run them for real, only
  governs what to do while they remain unrunnable.

**Status**: Adopted.

---

## ADR-010: `feature-planner` requires a `codebase-intelligence` report as a hard precondition, not optional context

**Decision**: Unlike every prior skill's stance toward composition
(`adversarial-diff-reviewer` and `acceptance-test-engineer` both treat a
`codebase-intelligence` report as optional composed context), `feature-
planner`'s engine requires a valid `codebase-intelligence` `report.json` as
an argument. A missing, unreadable, or schema-mismatched report is a
**failure condition** — the CLI exits non-zero with an actionable error —
not a degraded-but-working path. Established in Phase 4
([[03-architecture]], `skills/feature-planner/engine/ci_report_loader.py`).

- User Value: grounding "affected files" in real structural data (real
  imports/defs/dependency-graph signal) rather than the agent guessing
  plausible-looking paths is this skill's entire value proposition — a plan
  with fabricated file paths is actively worse than no plan, because it
  looks authoritative while being wrong.
- Correctness: `ci_report_loader.py` validates the report against the real
  `CodebaseIntelligenceReport` schema (via required-field access, raising
  `CiReportError` on `KeyError`) rather than silently proceeding with
  partial data.
- Security: no new surface — the loader is read-only, reads a report the
  agent already has read access to, and never executes or interprets its
  contents beyond structural field access.
- Simplicity: one clear rule (missing report -> hard failure) rather than a
  degraded "best-effort without composition" mode that would need its own
  testing and disclosure surface.
- Maintainability: `ci_report_loader.py` defines its own lightweight
  dataclasses rather than importing `codebase-intelligence`'s package
  directly — keeps `feature-planner` independently portable, same
  stdlib-only-per-skill discipline as ADR-006.
- Evidence: `examples/feature-planner/example-run.md` — a real dogfood run
  where the required report was genuinely regenerated and genuinely used;
  grounding the affected-files decision in it correctly identified the
  right target file despite an imperfect ranking (see L13 in
  [[12-known-limitations]]), and surfaced a real gap in a different skill
  (found via composition, not despite it).
- Future Evolution: this ADR does not mandate required composition
  universally — a future skill adopts mandatory composition only when the
  same "ungrounded output is actively harmful" argument applies to it
  specifically, not by default. It also does not, by itself, upgrade
  [[16-assumptions-and-validation]] A10's status — required composition is
  now real architecture, but Experiment B still needs an independent
  baseline to validate whether composition *outperforms* the alternative,
  per ADR-009.

**Status**: Adopted.

---

## ADR-011: `security-context-guard`'s engine classifies and recommends; it never authorizes

**Decision**: Extend ADR-008's redact-not-exclude discipline from
diff-content secrets specifically to a general classify/minimize/sanitize
engine covering secrets *and* PII *and* high-risk actions
(`skills/security-context-guard/`). Establish, as a hard rule rather than an
implicit convention, that this engine's `classification.suggested_verdict`
is always advisory — the deterministic engine never authorizes anything
itself; only the agent's Step 3 workflow, and ultimately a human, makes the
real authorization decision. On inconclusive input (no action description
given), the rollup defaults toward `REQUIRES_HUMAN_APPROVAL`, not
`AUTHORIZE` — fail closed, not fail open.

- User Value: a consistent, auditable classify/sanitize pass reduces the
  chance that a secret or PII value is accidentally echoed into a log, a
  tool call, or an external message, and gives every REQUIRES_HUMAN_APPROVAL
  recommendation a concrete evidence trail instead of an unexplained
  judgment call.
- Correctness: every secret/PII match is redacted (`pattern.regex.sub()`,
  every occurrence) before it reaches any model field, JSON, or Markdown
  output — verified by
  `tests/test_integration.py::test_secret_value_never_leaks_into_json_or_markdown`
  and its PII/action-text counterparts.
- Security: directly implements [[06-security-model]]'s Human Approval
  principle for a case no prior skill covered explicitly — a skill whose
  entire purpose is security classification must not become the thing that
  quietly authorizes a high-risk action. The engine's output type is a
  *recommendation*, never an executed gate; SKILL.md's Security Constraints
  and Human Checkpoints sections state this explicitly.
- Simplicity: one clear rule (advisory only, fail closed on uncertainty)
  rather than a graduated confidence/auto-approval scale that would invite
  the skill to creep into making real authorization decisions on its own.
- Maintainability: `classification.py` is a single ~55-line module
  containing the entire rollup rule, independently unit-tested
  (`tests/test_classification.py`) separately from the pattern-matching
  modules that feed it.
- Portability: composition with `codebase-intelligence` is deliberately kept
  **optional** here (unlike ADR-010) — this skill's engine covers content
  and actions generically, not something that becomes actively harmful
  without a structural map; ADR-010's own Future Evolution clause reserves
  mandatory composition for cases where ungrounded output is actively
  harmful, which doesn't apply here.
- Evidence: `examples/security-context-guard/example-run.md` — a real
  dogfood run against this phase's own source and a real pending
  `Publishing`-category decision (committing/pushing these files). The first
  run missed the action entirely due to a too-narrow proximity window in
  `action_patterns.py`; fixed same-session by switching to same-sentence
  co-occurrence matching (L16 in [[12-known-limitations]]), and re-verified
  correctly producing `REQUIRES_HUMAN_APPROVAL` afterward. This dogfood run
  also served as Pilot C toward [[16-assumptions-and-validation]] A7 — see
  [[17-experiment-viability-check]].
- Future Evolution: this ADR does not change what counts as a real
  authorization — a human (or an explicitly-authorized separate mechanism)
  still makes that call outside this skill entirely, exactly as before this
  skill existed. A future skill that also produces a recommendation-shaped
  output should follow the same "advisory only, fail closed" rule rather
  than reinventing it.

**Status**: Adopted.

---

## ADR-012: `root-cause-analyzer` reuses ADR-010's required-composition pattern a second time, plus a new tiered-evidence scoring rule

**Decision**: `root-cause-analyzer` (Phase 6) requires a `codebase-
intelligence` `report.json` as a hard precondition, the same way
`feature-planner` does (ADR-010) — a missing/malformed report is a failure
condition, not a degraded path. This is a **reuse** of ADR-010's rule, not a
new architectural decision on that point: two skills now share it, and a
future skill should default to reusing it too when the same "ungrounded
output is actively harmful" test applies, rather than re-deriving it.
What genuinely is new this phase: candidate locations are scored in two
explicit, non-blended **evidence tiers** —
`stack-trace` (a path parsed directly out of a real traceback/stack frame in
the symptom text) always outranks `keyword` (vocabulary overlap with a
module's path/names/docstring/imports), via a dominant flat score bonus
rather than a weighted blend. `evidence_tier` is carried as its own field
into every candidate, not collapsed into the score alone, so the agent's
Step 3 investigation can distinguish "the traceback literally names this
file" from "this file happens to share vocabulary with the bug report."

- User Value: a stack-trace-confirmed candidate is categorically better
  evidence than a keyword guess — blending them into one undifferentiated
  score (as a naive extension of `relevance_scorer.py` would) would let a
  few extra keyword hits outrank real evidence a runtime already handed the
  investigator for free.
- Correctness: `candidate_scorer.py`'s `_stack_trace_hits` does an exact/
  suffix path match against `stack_trace_parser.py`'s parsed frames, so a
  frame from a different repo or a vendored path (case-05 in
  `evaluations/root-cause-analyzer/`) correctly produces zero stack-trace
  hits rather than a false match — verified by
  `tests/test_candidate_scorer.py` and `tests/test_report.py`.
- Security: no new surface — both parsers are read-only pattern matching
  over already-provided text; same posture as every prior skill's
  deterministic layer.
- Simplicity: one dominant bonus constant (`_STACK_TRACE_BONUS = 100`)
  rather than a tunable weighting scheme between tiers — avoids inventing a
  confidence-calibration system this project has no evidence it needs yet.
- Maintainability: `stack_trace_parser.py` and `candidate_scorer.py` are
  separate, independently-tested modules (each <300 lines) — the trace-shape
  patterns can be extended later (e.g. a third language's traceback format)
  without touching the scoring logic.
- Portability: stdlib-only (same rationale as ADR-006); no cross-package
  import of `codebase-intelligence` (own `ci_report_loader.py` copy, same as
  ADR-010's `feature-planner` precedent).
- Evidence: `evaluations/root-cause-analyzer/` — 8 fixtures including one
  with a clean in-repo stack trace (case-01), one with a trace pointing
  outside the repo entirely (case-05), and one where a stack-trace hit
  competes against a high-fan-in hotspot module (case-08); all 8
  deterministic-layer cases score correctly. This is the **fifth**
  judgment-based skill evaluated this way, and the first whose judgment
  layer did **not** score perfect precision/recall on every fixture (case-03
  scored 0.67/0.67, not fabricated to look better — see
  `evaluations/root-cause-analyzer/RESULTS.md` and L8 in
  [[12-known-limitations]]).
- Future Evolution: this ADR does not generalize evidence tiering beyond
  stack-trace-vs-keyword; a future skill with its own strong, mechanically-
  verifiable evidence source (e.g. a real test-failure log, a CI run ID)
  should evaluate on its own merits whether a similar dominant-tier bonus
  is warranted, not assume this exact constant or shape.

**Status**: Adopted.

---

## ADR-013: `architecture-decision` reuses ADR-010's required-composition pattern a third time, plus a new per-option blast-radius scoring rule

**Decision**: `architecture-decision` (Phase 7) requires a `codebase-
intelligence` `report.json` as a hard precondition, the same way
`feature-planner` (ADR-010) and `root-cause-analyzer` (ADR-012) do — a
missing/malformed report is a failure condition, not a degraded path. This
is a **reuse** of ADR-010's rule for the third time, not a new
architectural decision on that point. What genuinely is new this phase:
each option parsed out of the decision text (`option_parser.py`) is scored
against `codebase-intelligence`'s real dependency graph via
`impact_scorer.py`, rolling keyword relevance up into a **blast-radius
tier** (`low`/`medium`/`high`) driven by real fan-in and hotspot data —
`hotspot_count > 0` or `blast_radius_score >= 10` forces `high`, regardless
of how many keywords matched. `blast_radius_tier` is carried as its own
field on every option's impact, not collapsed into a relevance number
alone, so the agent's Step 3 decision-record walk can distinguish "this
option touches code 15 other modules depend on" from "this option merely
shares some vocabulary with a module."

- User Value: a decision that would touch a real hotspot deserves wider
  review before it's finalized; a keyword-relevance number alone (as a
  naive extension of `feature-planner`'s or `root-cause-analyzer`'s
  scorers would produce) cannot express that distinction on its own —
  blast radius needs the dependency graph, not just text overlap.
- Correctness: `impact_scorer.py`'s `_blast_radius_tier` is a single, small,
  independently-tested function (`tests/test_impact_scorer.py`); an option
  with zero keyword matches produces zero impacted modules and a `low` tier
  with a `blast_radius_score` of 0, not a fabricated one (verified by
  `tests/test_report.py` and evaluation case-04/case-05's contrast between
  a real zero-impact leaf module and an ungrounded option).
- Security: no new surface — the scorer is read-only pattern matching over
  already-provided text and an already-loaded report; same posture as every
  prior skill's deterministic layer.
- Simplicity: one small tier function with two fixed thresholds
  (`_HIGH_BLAST_RADIUS = 10`, `_MEDIUM_BLAST_RADIUS = 3`) rather than a
  tunable weighting/calibration system this project has no evidence it
  needs yet — same "no invented confidence-calibration scheme" discipline
  ADR-012 already established for evidence tiering.
- Maintainability: `option_parser.py` and `impact_scorer.py` are separate,
  independently-tested modules (each under 300 lines) — the option-shape
  patterns (explicit markers, numbered lists, vs-split) can be extended
  later without touching the scoring logic.
- Portability: stdlib-only (same rationale as ADR-006); no cross-package
  import of `codebase-intelligence` (own `ci_report_loader.py` copy, same
  as ADR-010's and ADR-012's precedent).
- Evidence: `evaluations/architecture-decision/` — 8 fixtures, including
  one with a decision touching a real hotspot (case-04), one with a
  decision touching only a genuinely low-impact leaf module (case-05), and
  one with an ungrounded option that scores zero matched modules despite
  being the higher-risk path in the text (case-04's Option B); all 8
  deterministic-layer cases score correctly, and all 8 judgment-layer
  cases scored perfect precision/recall (unlike `root-cause-analyzer`'s
  Phase 6, which had one non-perfect case — stated here rather than implied
  away). The real dogfood run
  (`examples/architecture-decision/example-run.md`) found and fixed a real
  gap in the decision-quality scanner (the tradeoff pattern matched the
  noun form "tradeoff"/"trade-off" but not the verb form "trades X for Y",
  which the dogfood decision's own text used twice) same-session, and
  separately disclosed — without fixing — a sharper version of the
  shared-path-prefix keyword-collision limitation already logged as L14
  and L19: at full-repository scale, a decision *about the platform's own
  architecture* produces a nearly-uninformative blast-radius signal because
  its vocabulary overlaps the whole repo's vocabulary almost everywhere.
- Future Evolution: this ADR does not generalize blast-radius tiering
  beyond fan-in/hotspot signal; a future skill with a different real risk
  signal (e.g. test coverage percentage, deployment frequency) should
  evaluate on its own merits whether a similar tiering approach is
  warranted, not assume this exact threshold or shape. It also does not
  resolve the keyword-collision-at-scale limitation surfaced by the real
  dogfood run — a future revision could explore TF-IDF-style down-weighting
  of corpus-common terms, but that tradeoff (added complexity vs. a
  currently-disclosed, understood limitation) has not been evaluated
  against real evidence of need.

**Status**: Adopted.


---

## ADR-014: `refactoring-safety` reuses ADR-010's required-composition pattern a fourth time, plus a new per-target risk-tier + independent test-coverage signal

**Decision**: `refactoring-safety` (Phase 8) requires a `codebase-
intelligence` `report.json` as a hard precondition, the same way
`feature-planner` (ADR-010), `root-cause-analyzer` (ADR-012), and
`architecture-decision` (ADR-013) do — a missing/malformed report is a
failure condition, not a degraded path. This is a **reuse** of ADR-010's
rule a fourth time, not a new architectural decision on that point. What
genuinely is new this phase: each resolved refactor target
(`target_resolver.py`) is scored against `codebase-intelligence`'s real
dependency graph via `safety_scorer.py`, rolling operation type (boundary-
changing vs. internal-only) and fan-in/hotspot data up into a **risk
tier** (`low`/`medium`/`high`) — and, separately, an independently-computed
**test-coverage signal** (`test_coverage_scanner.py`, a static-import
heuristic: does any test-shaped module import the target) is checked
against that tier. When the tier is medium/high AND no covering test module
was found, a distinct `untested-blast-radius` flag fires — the two signals
are kept as separate fields (`risk_tier`, `test_coverage_modules`) rather
than blended into one number, so the agent's Step 3 checklist walk can
distinguish "structurally risky and verified" (evaluation case-01) from
"the text never mentions tests, but the codebase genuinely has coverage"
(case-03) from "structurally risky and genuinely unverified" (case-02/
case-04).

- User Value: a refactor whose target has real callers and no test coverage
  deserves a materially different response than one with the same fan-in
  but real test coverage — collapsing structural risk and verification
  status into one number (as a naive extension of ADR-013's blast-radius
  tier would) would hide exactly the distinction that matters most before
  executing a refactor.
- Correctness: `safety_scorer.py`'s `_structural_tier` is a single, small,
  independently-tested function (`tests/test_safety_scorer.py`) with
  separate bands for boundary-changing operations (scored against real
  fan-in) and internal-only operations (scored against hotspot status
  alone, since callers outside the target aren't directly affected by
  extract/inline); `test_coverage_scanner.py`'s heuristic is verified not
  to conflate "the refactor text never mentions tests" with "the target has
  no real test coverage" — these are independent signals that can and do
  diverge, verified explicitly by evaluation case-03's contrast.
- Security: no new surface — both the risk scorer and the test-coverage
  scanner are read-only pattern matching over already-provided text and an
  already-loaded report; same posture as every prior skill's deterministic
  layer.
- Simplicity: one small tier function with two fixed fan-in thresholds
  (`_HIGH_FAN_IN = 5`, `_MEDIUM_FAN_IN = 1`) rather than a tunable
  weighting/calibration system this project has no evidence it needs yet —
  same "no invented confidence-calibration scheme" discipline ADR-012 and
  ADR-013 already established.
- Maintainability: `target_resolver.py`, `test_coverage_scanner.py`, and
  `safety_scorer.py` are separate, independently-tested modules (each under
  300 lines) — the operation-type keyword table and the test-file naming
  convention can each be extended later without touching the other's logic.
- Portability: stdlib-only (same rationale as ADR-006); no cross-package
  import of `codebase-intelligence` (own `ci_report_loader.py` copy, same
  as ADR-010's, ADR-012's, and ADR-013's precedent).
- Evidence: `evaluations/refactoring-safety/` — 8 fixtures, including one
  where a structurally risky target is genuinely covered (case-01), one
  where the text never mentions tests but real coverage exists anyway
  (case-03), one where a hotspot delete has zero real coverage
  (case-04), and one contrasting pair (case-01 vs. case-06) exercising the
  same "unresolved target: expected-absent new name, or genuinely fake"
  ambiguity ADR-013 first surfaced for architecture-decision's zero-match
  options; all 8 deterministic-layer cases score correctly, and all 8
  judgment-layer cases scored perfect precision/recall. The real dogfood
  run (`examples/refactoring-safety/example-run.md`) — a genuine
  duplicated-helper refactor this phase's own build produced — disclosed,
  without fixing, a new cross-skill limitation (L22): `codebase-
  intelligence`'s own `fan_in` count undercounted a real caller (a test
  module using an absolute-style cross-package import) relative to this
  engine's own independent `caller_modules` scan, which found it correctly.
- Future Evolution: this ADR does not generalize risk tiering beyond
  operation-type + fan-in/hotspot signal, and does not extend test-coverage
  detection beyond static import presence (it does not run the test suite
  or check pass/fail status) — a future skill with a real CI test-result
  feed could score actual pass/fail rather than static presence, but that
  tradeoff has not been evaluated against real evidence of need. It also
  does not fix L22 — that gap lives in `codebase-intelligence`'s own
  dependency-graph construction (absolute-style cross-package imports not
  recognized as edges), out of scope for this skill to silently patch;
  `codebase-intelligence`'s own future revision should evaluate it on its
  own merits.

**Status**: Adopted.

---

## ADR-015: `regression-hunter` reuses ADR-010's required-composition pattern a fifth time, plus a new three-axis, non-blended regression-risk scoring rule

**Decision**: `regression-hunter` (Phase 9) requires a `codebase-
intelligence` `report.json` as a hard precondition, the same way
`feature-planner` (ADR-010), `root-cause-analyzer` (ADR-012),
`architecture-decision` (ADR-013), and `refactoring-safety` (ADR-014) do —
a missing/malformed report is a failure condition, not a degraded path.
This is a **reuse** of ADR-010's rule a fifth time, not a new architectural
decision on that point. What genuinely is new this phase: for each file
changed in a diff, three explicitly separate, non-blended regression
signals are computed and kept as three distinct fields, never collapsed
into one score — **Axis 1** (`diff_pattern_flags`, deterministic
regex/heuristic matches scanned directly against the diff's own hunks —
removed exception handling, a removed conditional guard with no
replacement, a large unreplaced deletion, decreased test assertions in a
changed test file, a modified function signature with no corresponding
test-file change in the same diff), **Axis 2** (`structural`, a blast-radius
tier resolved against `codebase-intelligence`'s real fan-in/hotspot data,
reusing `refactoring-safety`'s `target_resolver.py`/`safety_scorer.py`
pattern as an independent copy), and **Axis 3** (`test_coverage`, an
independently-computed static-import heuristic, reusing `refactoring-
safety`'s `test_coverage_scanner.py` pattern as an independent copy). A
documented rule table (`engine/risk_scorer.py`) then combines the three
axes into one `overall_risk_tier` per file — but the three underlying
fields remain visible and separately inspectable in every report, so the
agent's Step 3 walk can always tell "this file was flagged but is covered"
apart from "this file has real blast radius but nothing regex-detectable
fired" apart from "this file is both flagged and structurally risky with no
coverage at all."

- User Value: a diff review that blends mechanical pattern-matching,
  dependency-graph blast radius, and test-coverage presence into one opaque
  number would hide exactly the distinctions that change what a reviewer
  should do next — a flagged-but-covered file needs a different response
  than an unflagged-but-uncovered hotspot, and collapsing them into the same
  number (as a naive single-score extension of any prior skill's scorer
  would) makes that decision harder, not easier, to make correctly.
- Correctness: `risk_scorer.py`'s `overall_risk_tier` is a single, small,
  independently-tested function (`tests/test_risk_scorer.py`, 13 tests
  covering all nine branches of the documented rule table) with a fixed,
  stated combination table (a high structural tier stays HIGH unless both
  covered and flag-free, in which case it drops one tier to MEDIUM but never
  lower; medium/low structural tiers escalate one tier when a flag fires
  with no coverage, and otherwise follow the more conservative of the two
  remaining signals) — verified against 8 evaluation fixtures where the
  three axes are deliberately made to diverge (case-06/case-07 exercise a
  diff-level "no test file changed in this diff" flag firing at the same
  time the composed report shows the file genuinely has real coverage — the
  two signals are independent by design and can and do disagree).
- Security: no new surface — the diff parser (an independent copy of
  `adversarial-diff-reviewer`'s parsing conventions), the structural
  resolver, and the test-coverage scanner are all read-only pattern matching
  over already-provided text and an already-loaded report; same posture as
  every prior skill's deterministic layer. This skill never blocks or
  authorizes a merge (see `SKILL.md`'s Security Constraints), consistent
  with `security-context-guard`'s ADR-011 precedent for advisory-only
  engine output.
- Simplicity: one small, explicit combination table with two fixed fan-in
  thresholds (`_HIGH_FAN_IN = 5`, `_MEDIUM_FAN_IN = 1`, the same constants
  `refactoring-safety`'s `safety_scorer.py` already established) rather than
  a tunable weighting/calibration scheme this project has no evidence it
  needs yet — same "no invented confidence-calibration scheme" discipline
  ADR-012/013/014 already established for their own tiering decisions.
- Maintainability: `diff_parser.py`, `target_resolver.py`,
  `test_coverage_scanner.py`, `regression_patterns.py`,
  `regression_scanner.py`, and `risk_scorer.py` are six separate,
  independently-tested modules (each under 300 lines, max 181) — the
  diff-pattern table can be extended later, and the combination rule can be
  revisited, without touching each other's logic.
- Portability: stdlib-only (same rationale as ADR-006); no cross-package
  import of `codebase-intelligence`, `refactoring-safety`, or
  `adversarial-diff-reviewer` (own `ci_report_loader.py`, `target_resolver.py`,
  `test_coverage_scanner.py`, and `diff_parser.py` copies, same portability
  discipline as ADR-010's, ADR-012's, ADR-013's, and ADR-014's precedent).
- Evidence: `evaluations/regression-hunter/` — 8 fixtures, including one
  where a flagged file is genuinely covered and a medium structural tier
  stays at medium rather than escalating (case-03), one where the identical
  medium structural tier with a flag AND no coverage escalates to HIGH
  (case-04), one where a high structural (hotspot) tier stays HIGH
  regardless of coverage once a flag fires (case-02), and one multi-file
  diff exercising per-file tier aggregation and stats independently
  (case-08); all 8 deterministic-layer cases score correctly, and all 8
  judgment-layer cases scored perfect precision/recall. The real dogfood
  run (`examples/regression-hunter/example-run.md`) — a genuine,
  already-tested `codebase-intelligence` scanner fix this phase's own build
  produced (excluding `*.egg-info` directories from repo scans) — correctly
  scored both changed files LOW risk (a purely additive, already-tested
  change to a moderate-fan-in module), and disclosed, without fixing, a new
  cross-skill limitation (L23): `target_resolver.py`'s substring-based
  caller-identification heuristic (shared, as an independent copy, with
  `refactoring-safety`'s identical pattern) produces a wildly inflated
  caller list for any module whose stem is a short, common word (`scanner`
  matched `testability_scanner`, `decision_scanner`, `safety_scanner`, and
  four other skills' own scanner modules) — the same coincidental-substring-
  collision mechanism already disclosed as L14/L19/L21, now shown for the
  first time in structural caller identification rather than keyword
  relevance ranking, and shown for the first time to affect two skills'
  independent copies of the same heuristic simultaneously.
- Future Evolution: this ADR does not generalize the three-axis pattern
  beyond diff-pattern/structural/coverage; a future skill with its own
  distinct, real, independently-computed signals should evaluate on its own
  merits whether a similar non-blended, rule-table combination is
  warranted, not assume this exact table or axis count. It also does not
  fix L23 — the substring-collision caller-identification gap is now known
  to affect at least two skills' independent copies of the same resolution
  heuristic; a future revision of that shared *pattern* (not a shared
  module — this project deliberately keeps no cross-skill imports) could
  require a word-boundary or dotted-segment match instead of a bare
  substring check, but that tradeoff has not been evaluated against other
  evidence of need across the skills that use it.

**Status**: Adopted.

---

## ADR-016: `release-readiness` reuses ADR-010's required-composition pattern a sixth time, plus a new Release Readiness Scorecard combining three always-available axes and two optional, cross-skill-composed ones

**Decision**: `release-readiness` (Phase 10, the final skill in the
Engineering Lifecycle group) requires a `codebase-intelligence`
`report.json` as a hard precondition, the same way `feature-planner`
(ADR-010), `root-cause-analyzer` (ADR-012), `architecture-decision`
(ADR-013), `refactoring-safety` (ADR-014), and `regression-hunter`
(ADR-015) do — a missing/malformed report is a failure condition, not a
degraded path. This is a **reuse** of ADR-010's rule a sixth time, not a
new architectural decision on that point. What genuinely is new this
phase: for each file changed in a diff, three explicitly separate,
always-available, non-blended signals are computed into a per-file
`readiness_tier` via a documented rule table — **Axis 1**
(`hygiene_flags`, deterministic release-blocking anti-patterns scanned
directly against the diff's own hunks — debug leftovers, merge-conflict
markers, hardcoded-secret-shaped literals, TODO-blocking markers), **Axis
2** (`structural`, a blast-radius tier resolved against `codebase-
intelligence`'s real fan-in/hotspot data, reusing `regression-hunter`'s
`target_resolver.py` pattern as a THIRD independent copy), and **Axis 3**
(`test_coverage`, an independently-computed static-import heuristic, a
third independent copy of the same pattern). The rule table: any hygiene
flag → `blocked`; high structural tier with no coverage → `blocked`; high
or medium structural tier, or no coverage → `needs-review`; otherwise
`clear`. Per-file tiers roll up into one report-level `overall_verdict`
(`NOT_READY` if any file is `blocked`, `READY_WITH_CONDITIONS` if any file
is `needs-review`, `READY` otherwise). Separately, this skill is the FIRST
in this platform to also compose OPTIONALLY with two other skills' own
`report.json` outputs — **Axis 4** (`regression_evidence`, surfaced
verbatim from a supplied `regression-hunter` report) and **Axis 5**
(`security_evidence`, surfaced verbatim from a supplied
`security-context-guard` report) — reusing `security-context-guard`'s
ADR-011 precedent for *optional* composition (missing/malformed input is a
warning, not a failure), explicitly NOT ADR-010's mandatory rule, for
these two specifically. Axis 4/5 evidence is surfaced as distinct fields
but deliberately does **not** feed the readiness rule table — each is
already a rolled-up verdict from a DIFFERENT skill's own rule table
(ADR-015 for regression risk, the security classification rollup for
security posture), and re-blending an already-rolled-up verdict from one
skill's engine into another skill's rule table would hide which skill
actually produced which judgment. `overall_verdict` is explicitly and
repeatedly framed everywhere (SKILL.md's Security Constraints/Human
Checkpoints, docstrings, README) as a recommendation for a human to
review, **never** an autonomous release gate — reusing ADR-011's
advisory-only discipline, extended here to this portfolio's single
highest-stakes recommendation.

- User Value: a human deciding whether a body of work is ready to ship
  currently has to eyeball several separate skills' reports, or accept one
  blended score that hides exactly the distinction that matters — a file
  with zero hygiene issues but no coverage on a real hotspot is a
  fundamentally different risk than a file with a leftover `print()`
  statement in an otherwise low-risk change (evaluation case-02 vs.
  case-03 exercise this directly). Composing OPTIONALLY with two other
  skills' real outputs, rather than re-deriving regression/security
  judgment from scratch, avoids contradicting work those skills already
  did correctly.
- Correctness: `readiness_scorer.py`'s rule table is a single, small,
  independently-tested function (`tests/test_readiness_scorer.py`, 12
  tests covering every branch, including the absolute-blocker-regardless-
  of-everything-else case and the empty-file-list default); the optional
  loaders (`regression_report_loader.py`, `security_report_loader.py`)
  are verified not to raise on missing/malformed input, only to warn
  (`tests/test_regression_report_loader.py`,
  `tests/test_security_report_loader.py`) — verified against 8 evaluation
  fixtures where at least two (case-03, case-07) deliberately exercise
  real divergence: case-03 has ZERO hygiene flags but is still `blocked`
  from Axis 2/3 alone; case-07 has a `clear` readiness_tier from Axes 1-3
  while a composed `regression-hunter` report shows `overall_risk_tier:
  high` for the same file — the two are surfaced as separate fields by
  design, never blended.
- Security: no new surface — the diff parser (a fourth independent copy of
  `adversarial-diff-reviewer`'s/`regression-hunter`'s parsing conventions),
  the structural resolver, the test-coverage scanner, and the two optional
  report loaders are all read-only pattern matching over already-provided
  text and already-loaded reports; same posture as every prior skill's
  deterministic layer. This skill never blocks or authorizes a release
  (see `SKILL.md`'s Security Constraints), consistent with
  `security-context-guard`'s ADR-011 precedent for advisory-only engine
  output — stated with extra emphasis here because "release verdict" is
  exactly the kind of high-stakes recommendation
  `project-memory-bank/06-security-model.md`'s Human Approval principle
  exists for.
- Simplicity: one small, explicit rule table combining exactly three
  always-available axes, with two optional axes deliberately excluded from
  it rather than folded in via a special case — avoids a combinatorial
  five-axis rule table this project has no evidence it needs, and keeps
  the "which skill produced which judgment" attribution clean.
- Maintainability: `diff_parser.py`, `hygiene_patterns.py`,
  `hygiene_scanner.py`, `target_resolver.py`, `blast_radius_scorer.py`,
  `test_coverage_scanner.py`, `regression_report_loader.py`,
  `security_report_loader.py`, and `readiness_scorer.py` are nine
  separate, independently-tested modules (each under 300 lines, max 211)
  — the hygiene-pattern table can be extended later, and the rule table
  can be revisited, without touching each other's logic.
- Portability: stdlib-only (same rationale as ADR-006); no cross-package
  import of `codebase-intelligence`, `regression-hunter`, or
  `security-context-guard` (own `ci_report_loader.py`, `diff_parser.py`,
  `target_resolver.py`, `test_coverage_scanner.py`,
  `regression_report_loader.py`, and `security_report_loader.py` copies,
  same portability discipline as every prior composing skill's precedent).
- Evidence: `evaluations/release-readiness/` — 8 fixtures, including one
  where a hygiene flag blocks a low-structural-risk, covered file anyway
  (case-02, an absolute-blocker demonstration), one where a completely
  clean diff (zero hygiene flags) still lands on `blocked` from Axis 2/3
  alone (case-03), a contrasting covered-hotspot case landing on
  `needs-review` instead (case-04), a merge-conflict-marker case (case-06),
  a composed-regression-evidence divergence case (case-07), and a
  multi-file mixed-tier case with a composed security report (case-08);
  all 8 deterministic-layer cases score correctly, and all 8 judgment-layer
  cases scored perfect precision/recall. The real dogfood run
  (`examples/release-readiness/example-run.md`) — a real, staged-then-
  unstaged (never committed) `git diff` of this phase's own 78 new files —
  confirmed a predicted false-positive shape concretely (a legitimate CLI
  `print()` flagged as a debug leftover) and surfaced, without fixing, a
  new, more consequential manifestation of the L14/L19/L21/L23
  substring-collision limitation class: `target_resolver.py`'s stem-based
  matching, reused unmodified inside `test_coverage_scanner.py`, produced
  false-positive **test coverage**, not just an inflated caller list, for
  modules whose stem collides with an identically-named module in an
  unrelated skill (L24 in [[12-known-limitations]]).
- Future Evolution: this ADR does not generalize the always-available/
  optional axis split beyond this skill's specific five axes; a future
  skill composing with more than one other skill's output should evaluate
  on its own merits whether the same "surface, don't re-blend"
  discipline applies, not assume this exact axis count or rule table. It
  also does not fix L23/L24 — the substring-collision resolution gap is
  now known to affect THREE skills' independent copies of the same
  pattern, and to produce both an inflated caller list (L23) and a
  false-positive coverage signal (L24); a future revision of that shared
  *pattern* (not a shared module) could require a word-boundary,
  dotted-segment, or same-skill-path-prefix-scoped match instead of a bare
  substring check, but that tradeoff has not been evaluated against other
  evidence of need across every skill that uses it — this is now the
  strongest case yet in this project for revisiting that tradeoff before a
  fourth skill copies the same pattern again.

**Status**: Adopted.

---

## ADR-017: `dependency-supply-chain` reuses ADR-010's required-composition pattern a seventh time, declines to build a live-vulnerability-DB or per-dependency-license feature, and reuses ADR-011's advisory/fail-closed discipline

**Decision**: `dependency-supply-chain` (Phase 11) requires a
`codebase-intelligence` `report.json` as a hard precondition, the same way
`feature-planner` (ADR-010), `root-cause-analyzer` (ADR-012),
`architecture-decision` (ADR-013), `refactoring-safety` (ADR-014),
`regression-hunter` (ADR-015), and `release-readiness` (ADR-016) do — a
missing/malformed report is a failure condition, not a degraded path. This
is a **reuse** of ADR-010's rule a seventh time. This skill reuses CI's
already-parsed `external_dependencies` field rather than re-parsing
manifests itself, to avoid an eleventh copy of manifest-parsing logic and
to inherit (documented, not hidden) CI's existing root-level-only scope
(L2). Two scope decisions are new and explicit:

1. **No live CVE/vulnerability-database lookup.** This project makes no
   network calls (ADR-006, stdlib-only, offline). A "supply-chain" skill
   without one is a real, narrower thing than a Snyk/Dependabot-style
   scanner — this is disclosed everywhere the skill is described (SKILL.md
   When NOT to Use, Known Limitations), not silently implied to be more
   than it is.
2. **No per-dependency license-risk detection**, despite this being in the
   original plan for this phase. Corrected during implementation: a
   manifest's own `license` field (in `package.json`/`pyproject.toml`)
   describes the *project's* license, not each declared dependency's —
   codebase-intelligence's `external_deps.py` does not capture per-
   dependency license data at all, and getting it would require inspecting
   installed package metadata (site-packages/`node_modules`), which is not
   guaranteed to exist and would make this skill's output depend on the
   target environment's install state rather than its declared manifests.
   Shipping a "license risk" flag from data that doesn't exist would be
   exactly the kind of ungrounded, plausible-looking output ADR-010 exists
   to prevent — so it was dropped from scope rather than faked, and named
   explicitly in Known Limitations as a future-evolution item instead of
   silently disappearing from the plan.

`suggested_risk_level` reuses `security-context-guard`'s ADR-011 advisory/
fail-closed discipline: it never blocks a merge or install itself (only a
human, via the agent's workflow, decides), and it fails closed to
`REQUIRES_REVIEW` — not `CLEAR` — whenever zero dependencies are found or
the CI report carried warnings, because a zero-dependency result is
ambiguous (genuinely no deps, vs. deps CI's parser didn't see) rather than
proof of a clean supply chain.

- User Value: turns "no one looks at `requirements.txt` until something
  breaks" into three concrete, offline-checkable, verifiable-by-citation
  signals (pin status, a five-entry known-risk-name table each citing a
  real public incident, duplicate/conflicting version declarations) plus an
  aggregate surface-area stat — without pretending to be a vulnerability
  scanner it isn't.
- Correctness: `pin_checker.py`'s classification (missing/wildcard/range/
  pinned) is unit-tested against both pip-style (`==`, `>=`) and npm-style
  (`^`, `~`, `x`) specifiers; `risk_patterns.py`'s known-risk table matches
  by exact lowercased name, not substring (`test_matches_are_exact_not_
  substring` explicitly guards against a `request`/`requests` false
  positive — the same word-boundary-precision discipline as the project's
  L23 fix, applied here from the start rather than found via dogfooding
  later); `duplicate_detector.py` is verified to fire only on genuinely
  conflicting version strings, not merely repeated identical declarations.
  8/8 evaluation fixtures score correctly on both layers (deterministic
  flag-set + risk-level, and this session's actual judgment-layer
  derivation) — disclosed with the same self-authored/single-rater caveat
  as every prior judgment skill (L8, now tenth time).
- Security: read-only; no network calls, no package-manager invocation, no
  installation/upgrade/removal of anything. `suggested_risk_level` is
  advisory-only per ADR-011's precedent, stated explicitly in SKILL.md's
  Security Constraints.
- Simplicity: 11 engine files (not the originally-planned 13 — no
  `license_patterns.py`, and `stats.py`/`surface_area.py` stayed separate
  as planned since they answer genuinely different questions), all under
  100 lines, orchestrated by one `scanner.py` and one `report.py`.
- Maintainability: each detector (`pin_checker.py`, `risk_patterns.py`,
  `duplicate_detector.py`) is independently testable and extensible (the
  known-risk table can grow without touching pin-status logic).
- Portability: stdlib-only; own `ci_report_loader.py` copy, no
  cross-package import of `codebase-intelligence` (same discipline as
  every prior composing skill).
- Evidence: `evaluations/dependency-supply-chain/` — 8 fixtures (clean/
  pinned, range-unpinned, known-risk-name, wildcard, duplicate-conflict,
  large surface area, a compounding multi-flag case, and the zero-
  dependency fail-closed case) — all correct on both layers. Real dogfood
  (`examples/dependency-supply-chain/example-run.md`) against this
  repo's own root manifest concretely demonstrated the inherited L2
  scope limitation: only 1 dependency (`pytest`) is visible from repo
  root, because the platform's ten skills' own dependencies live one
  level down in `skills/*/pyproject.toml`, which CI's parser doesn't
  recursively scan.
- Future Evolution: real CVE-lookup integration and real per-dependency
  license detection are both named, disclosed future-evolution items, not
  silently deferred — either would require a genuinely new capability
  (network access, or installed-package metadata inspection) this project
  has deliberately not built, and should be evaluated against real evidence
  of need (an actual user hitting this gap) before being added, per this
  project's standing adaptive-roadmap rule.

**Status**: Adopted. Note on process: this phase was started at the user's
explicit direction on 2026-08-26, reopening the roadmap freeze the
mentor-review pass (same date, this file's context) had put in place — A2
and A5 remain `UNKNOWN`; starting this phase is not new external-validation
evidence and is not presented as such (see
[[16-assumptions-and-validation]]).

---

## ADR-018: `engineering-knowledge-capture` reuses ADR-010's required-composition pattern an eighth time, builds its word-boundary resolver correct from day one, and is the first skill whose deterministic layer targets a documentation artifact rather than a code-risk judgment

**Decision**: `engineering-knowledge-capture` (Phase 12) requires a
`codebase-intelligence` `report.json` as a hard precondition, the same way
`feature-planner` (ADR-010) through `dependency-supply-chain` (ADR-017) do
— a missing/malformed report is a failure condition, not a degraded path.
This is a **reuse** of ADR-010's rule an EIGHTH time. Three things are new
and explicit:

1. **`location_resolver.py` is the fourth independent copy of the
   word-boundary-aware containment check** first added to
   `target_resolver.py` in `refactoring-safety`/`regression-hunter`/
   `release-readiness` — but this is the FIRST copy built with the fix
   from day one, rather than shipped with the bare-substring bug
   ([[12-known-limitations|L23]]/[[12-known-limitations|L24]]) and fixed
   later. Cross-referenced explicitly in the module's own docstring, not
   presented as a novel technique.
2. **`priority_scorer.py` reuses `security-context-guard`'s (ADR-011) and
   `dependency-supply-chain`'s (ADR-017) fail-closed-under-uncertainty
   discipline**, adapted for this skill's shape: an unresolved candidate,
   or one scored against a CI report that itself carried a warning, fails
   closed to `MEDIUM` — never silently `LOW`. Unlike those two prior
   skills, this version's scorer additionally never assigns `LOW` at all,
   even for a resolved-but-structurally-unremarkable candidate (real
   module, zero fan-in, not a hotspot) — a deliberate, disclosed choice to
   fail upward (review one extra candidate) rather than downward (miss a
   real one), since missing a candidate for capture is this skill's worst
   failure mode, not reviewing a low-value one.
3. **This is the first skill in the portfolio whose deterministic layer's
   job is to find candidates for a *documentation artifact*** (an ADR /
   known-limitation / lessons-learned entry in this project's own memory
   bank) rather than a code-risk or process-quality judgment. It never
   writes into `project-memory-bank/` itself — the engine only flags
   candidates; drafting and committing the actual entry stays a
   human/agent-checkpointed step, the same Human Approval principle
   [[06-security-model]] already establishes for every other advisory
   skill's verdict.

A real dogfood run (`examples/engineering-knowledge-capture/example-run.md`)
against genuine excerpts of this project's own engineering history found a
real, disclosed-not-fixed limitation: `location_resolver.py` only searches
the exact matched line for a module mention, not the surrounding
paragraph, so a real narrative that names a module in one sentence and
states the decision/lesson in an adjacent sentence does not resolve — see
[[12-known-limitations|L28]].

- User Value: formalizes an activity this project already does informally
  every phase (ADRs, L-numbers, lessons-learned) into a runnable first-pass
  candidate finder, reducing the chance a real decision/lesson goes
  uncaptured simply because writing it up was skipped under time pressure.
- Correctness: candidates are leads, never verdicts — the agent's Step 3
  Knowledge Capture Checklist ([[05-evaluation-framework]]) is the only
  place a candidate becomes an actual entry.
- Security: read-only; never writes to `project-memory-bank/`; no network
  calls.
- Simplicity: reuses Pattern 2 (ADR-007, eleventh reuse) and ADR-010
  (eighth reuse) rather than inventing new architecture.
- Maintainability: engine files land under 130 lines each (max
  `knowledge_patterns.py` at 121), consistent with this project's
  <300-line-per-file discipline.
- Portability: `location_resolver.py` is an independent copy, no
  cross-skill import, matching every prior composing skill's pattern.
- Evidence: L8 applies an eleventh time (self-authored, single-rater
  judgment-layer evaluation); no assumption in
  [[16-assumptions-and-validation]] is upgraded by shipping this skill.
- Future Evolution: the single-line resolution window (L28) and the
  never-assigned `LOW` band are both named as candidates for future
  refinement, not solved speculatively here without real evidence of need.

**Status**: Adopted. Note on process: this phase was started at the user's
explicit direction on 2026-08-26, reopening the roadmap freeze the
mentor-review pass (same date, this file's context) had put in place a
SECOND time (Phase 11 was the first reopening) — A2 and A5 remain
`UNKNOWN`; starting this phase is not new external-validation evidence and
is not presented as such (see [[16-assumptions-and-validation]]).

---

## ADR-019: `context-optimizer` reuses ADR-010's required-composition pattern a ninth time, builds its relevance scorer with a tokenized (not `\b`-regex) whole-token check, and inverts the fail-closed-toward-caution convention into a fail-OPEN-toward-inclusion default

**Decision**: `context-optimizer` (Phase 13) requires a
`codebase-intelligence` `report.json` as a hard precondition, the same way
`feature-planner` (ADR-010) through `engineering-knowledge-capture`
(ADR-018) do — a missing/malformed report is a failure condition, not a
degraded path. This is a **reuse** of ADR-010's rule a NINTH time. Three
things are new and explicit:

1. **`relevance_scorer.py` is the fifth independent copy of a whole-token
   containment check** in the L23/L24 lineage — but unlike
   `location_resolver.py` (Phase 12's fourth copy, a `\bstem\b` regex), it
   tokenizes both sides on `_`/`/`/`.`/`-` and checks exact token-set
   membership. This is a deliberate, disclosed departure from copying
   `location_resolver.py` verbatim, not an oversight: `\b` never produces
   a boundary inside a snake_case identifier (`\w` includes `_`), so it
   would never match a single-word keyword like "resolver" against
   `location_resolver.py` at all — too strict for a skill that scores many
   files by relevance rather than resolving to one canonical location.
   Tokenizing trades some of that strictness for real recall (a keyword
   can match one real component of a compound filename), at the disclosed
   cost that it can also match a filename where that component is only
   part of a longer, less-related identifier — see
   `engine/relevance_scorer.py`'s own docstring and SKILL.md Known
   Limitations for the full reasoning.
2. **`budget_selector.py` inverts the fail-closed-toward-caution
   convention** ADR-011 (`security-context-guard`), ADR-017
   (`dependency-supply-chain`), and ADR-018 (`engineering-knowledge-
   capture`) established. Those skills fail closed toward *caution*
   because under-flagging a risk or an unresolved candidate is the worse
   failure. Here the worse failure runs the other way: silently
   *excluding* a file the task actually needed breaks the downstream
   work, while recommending one extra file only costs some budget — so
   under uncertainty (a low-but-nonzero relevance score, or a single file
   whose own size exceeds the budget alone) this skill fails **open**
   toward inclusion instead. Framed explicitly as the same underlying
   principle (fail toward whichever error is cheaper to recover from)
   applied to a domain where the cheaper error points the other way, not
   a silent departure from precedent.
3. **`estimated_tokens` is a disclosed, crude line-count heuristic, not a
   real tokenizer** — this project makes no network calls (ADR-006), so no
   `tiktoken`-class dependency is available or appropriate. Stated as
   order-of-magnitude only, never as an exact budget guarantee, in
   `size_estimator.py`'s docstring and SKILL.md Known Limitations, up
   front rather than discovered later.

A real dogfood run (`examples/context-optimizer/example-run.md`) against
this repo's own current state, using a real task description from this
actual session, found a real, disclosed-not-fixed limitation: at
full-repository scale, keyword relevance floods with false-positive CORE
recommendations when the task description is phrased in this project's
own recurring vocabulary (shared documentation/evaluation-harness
boilerplate repeated across every skill) — 5 of 17 CORE recommendations in
the dogfood run were unrelated files, not `context-optimizer` files. This
is a new manifestation of the same mechanism class `architecture-
decision`'s L14/L19/L21 already disclosed — see
[[12-known-limitations|L29]].

- User Value: turns "read everything speculatively, or guess from
  filenames alone" into a ranked, budget-aware recommendation grounded in
  real file/module/dependency data — directly on-theme with this
  project's own standing <300-line-per-file modularity discipline the
  user restated when directing this phase.
- Correctness: recommendations are leads, never a claim of completeness —
  the agent's Step 3 Context Optimization Checklist
  ([[05-evaluation-framework]]) is the only place the recommended set is
  actually judged sufficient for the task.
- Security: read-only; never loads any file into any actual context
  window; no network calls.
- Simplicity: reuses Pattern 2 (ADR-007, twelfth reuse) and ADR-010 (ninth
  reuse) rather than inventing new architecture.
- Maintainability: engine files land under 100 lines each (max
  `models.py` at 95), consistent with this project's <300-line-per-file
  discipline.
- Portability: `ci_report_loader.py` is an independent copy, no
  cross-skill import, matching every prior composing skill's pattern.
- Evidence: L8 applies a twelfth time (self-authored, single-rater
  judgment-layer evaluation, still perfect scores on all 8 fixtures — see
  [[12-known-limitations]]); no assumption in
  [[16-assumptions-and-validation]] is upgraded by shipping this skill.
- Future Evolution: L29's full-repository-scale keyword-flooding finding
  and the crude token-estimate heuristic are both named as candidates for
  future refinement (TF-IDF-style down-weighting, or a real tokenizer),
  not solved speculatively here without real evidence of need beyond one
  dogfood run.

**Status**: Adopted. Note on process: this phase was started at the user's
explicit direction on 2026-08-26, reopening the roadmap freeze the
mentor-review pass (same date, this file's context) had put in place a
THIRD time (Phase 11 and Phase 12 were the first two reopenings) — A2 and
A5 remain `UNKNOWN`; starting this phase is not new external-validation
evidence and is not presented as such, and this tension is now deferred
across three consecutive phase boundaries (see
[[16-assumptions-and-validation]]).

---

## ADR-020: `workflow-composer` reuses ADR-010's required-composition pattern a tenth time, is the first skill whose engine executes other skills' real code, and fails CLOSED on execution uncertainty — the opposite default from ADR-019

**Decision**: `workflow-composer` (Phase 14) ships with a hardcoded
registry of exactly 3 workflow templates
(`understand-then-plan`, `understand-then-test-plan`,
`understand-then-optimize-context`), every one of which requires a
`codebase-intelligence` `report.json` as its first, mandatory step — the
same hard-precondition discipline `feature-planner` (ADR-010) through
`context-optimizer` (ADR-019) established. This is a **reuse** of
ADR-010's rule a TENTH time. Four things are new and explicit:

1. **First skill whose engine invokes other skills' real code.** Every
   prior skill in this portfolio analyzes a static artifact
   (`codebase-intelligence`'s report, a diff, a requirement, another
   skill's own report). `workflow-composer` is the first whose
   deliverable is composed *execution*: `step_runner.py` subprocess-runs
   `python -m engine.cli ...` against each named skill's own directory
   for real. Named explicitly as a new skill category, the same way
   ADR-018 flagged `engineering-knowledge-capture`'s "documentation
   artifact, not a code-risk judgment" category shift.
2. **The registry is deliberately hardcoded, not a generic chainer.**
   All 3 templates reuse a composition this project already ran for real
   in an earlier phase's dogfood (`understand-then-plan` reuses Phase 4's;
   `understand-then-test-plan` reproduces Phase 3's real Pilot B
   composition, including its `TEXT_APPEND` wiring — `acceptance-test-
   engineer`'s CLI has no `--ci-report`-style flag, confirmed by reading
   its shipped `engine/cli.py`, not assumed; `understand-then-optimize-
   context` reuses Phase 13's). A new template requires a code change and
   a real dogfood run, not a config edit — this bounds the blast radius of
   an untested composition being shipped as if validated.
3. **`executor.py` fails CLOSED, not open — the opposite default from
   ADR-019, on purpose.** `context-optimizer` (ADR-019, one phase earlier)
   inverted this project's fail-closed-toward-caution convention because
   under-recommending context was its cheaper-to-avoid failure. Here the
   answer points back the normal direction: building further steps on top
   of a failed or drifted upstream step is the expensive failure (wasted
   compute, a corrupted or misleading downstream report), not the cheap
   one — so a step's non-zero exit or malformed output stops the chain
   immediately (remaining steps marked `SKIPPED`), and a pre-execution
   `compatibility_checker.py` drift finding blocks all real execution
   outright before any subprocess runs at all. Framed explicitly as the
   *same* underlying principle as ADR-019 (fail toward whichever error is
   cheaper to recover from) landing on the opposite default because the
   cheaper error points the opposite way in this domain — not a silent
   inconsistency with the phase immediately before it.
4. **The compatibility checker is a textual drift guard, not real schema
   validation.** It confirms the upstream skill's name still appears in
   the downstream skill's SKILL.md Preconditions/Required Context
   sections — cheap, real, and disclosed as unable to catch a wiring-mode
   error (declaring `CLI_FLAG` for a skill whose CLI has no such flag) if
   the marker string itself is still textually present; that class of bug
   would only surface as a real subprocess failure at run time, which the
   fail-closed executor still catches, just later than the pre-execution
   gate would.

A real dogfood run (`examples/workflow-composer/example-run.md`) against
this repo's own current (fourteen-skill) state, using a real task
description from this actual session, found a real, disclosed-not-fixed
finding: `feature-planner`'s own relevance scorer (part of its real
output, not something `workflow-composer` computes) ranked a test file
(`skills/workflow-composer/tests/test_real_execution.py`) as the single
highest-scoring file in the entire 1,010-file repository — ahead of every
real engine implementation file relevant to the task. This is the same
keyword-flooding mechanism class `architecture-decision` (L14/L19/L21)
and `context-optimizer` (L29) already disclosed, but the first time it
was observed directly inside `feature-planner`'s own scorer rather than
`context-optimizer`'s — confirming the susceptibility is shared across
every keyword-relevance engine in this portfolio, not specific to one
skill's scorer design. `workflow-composer` composes with `feature-planner`
as-is; it does not filter or improve the composed skill's own output —
see [[12-known-limitations|L30]].

- User Value: mechanizes a pattern this project's own engineers already
  proved out by hand three separate times (Pilot B, Phase 4's dogfood,
  Phase 13's dogfood) into a real, re-runnable chain, instead of a human
  manually copying file paths between CLI invocations.
- Correctness: every step result traces to a real subprocess exit code
  and a real output file, never a simulated or assumed status; the
  `--dry-run` path validates registry lookup and compatibility checking
  without ever claiming a subprocess ran when it didn't.
- Security: every composed skill stays read-only/advisory against the
  target repo; this executor only ever writes report files under
  `--out-dir`; no network calls; no shell/eval of caller-supplied
  strings — every subprocess argv is built from typed `WorkflowStep`
  fields.
- Simplicity: reuses Pattern 2 (ADR-007, thirteenth reuse) and ADR-010
  (tenth reuse) rather than inventing new architecture; the registry's
  hardcoded scope is itself a simplicity choice over a generic composer.
- Maintainability: engine files land under 300 lines each (max
  `step_runner.py` at 152 lines), consistent with this project's
  <300-line-per-file discipline, restated explicitly by the user when
  directing this phase.
- Portability: no cross-skill Python imports — every composed skill is
  invoked as an isolated subprocess via its own CLI, the same boundary
  every prior composing skill's `ci_report_loader.py`-style independent
  copy already established, taken one step further (process isolation,
  not just code isolation).
- Evidence: L8 applies a thirteenth time (self-authored, single-rater
  judgment-layer evaluation, perfect scores on all 8 fixtures — see
  [[12-known-limitations]]); no assumption in
  [[16-assumptions-and-validation]] is upgraded by shipping this skill —
  A10 in particular stays `UNKNOWN` despite this phase directly overriding
  its "do not build" decision (see Status below).
- Future Evolution: L30's cross-skill keyword-flooding finding strengthens
  (does not newly create) the case for eventually addressing the shared
  mechanism class named across L14/L19/L21/L29/L30, rather than treating
  each instance as isolated; not solved speculatively here.

**Status**: Adopted. Note on process: this phase was started at the
user's explicit direction on 2026-08-26, reopening the roadmap freeze a
FOURTH time (Phase 11, Phase 12, and Phase 13 were the first three
reopenings) — and, unlike those three, this reopening also directly
overrides a **named, phase-specific** decision already on record:
[[16-assumptions-and-validation]] A10 states "do not build Workflow
Composer (Phase 14) until Experiment B can be run," and this ADR-009
warns explicitly against letting an internal pilot substitute for that
real experiment. A2, A5, and A10 all remain `UNKNOWN`; starting this
phase is not new external-validation evidence for any of them and is not
presented as such. This tension is now deferred across four consecutive
phase boundaries, the first of which overrode a decision naming the
overridden phase by number.

## ADR-021: `engineering-memory` reuses ADR-010's required-composition pattern an eleventh time, and is the first skill whose primary retrieval corpus is this project's own memory bank rather than a target repo's external artifacts

**Decision**: `engineering-memory` (Phase 15) requires a
`codebase-intelligence` `report.json` as a hard precondition (ADR-010,
reused an ELEVENTH time — used only to resolve module mentions inside
retrieved records, not to drive retrieval itself), but its **primary**
input corpus is `project-memory-bank/11-decisions.md` and
`12-known-limitations.md` — this project's own memory bank. Three things
are new and explicit:

1. **First "self-referential composition" in the portfolio.** Every prior
   composing skill (`feature-planner` through `workflow-composer`)
   analyzes a target repo's own code, diffs, or another skill's report
   about that target repo. `engineering-memory` instead retrieves against
   this project's own recorded ADRs and limitations — the corpus is about
   the skills platform itself, not whatever repo `--ci-report` happens to
   point at. Named explicitly as a new composition category, the same way
   ADR-018 and ADR-020 named their own category shifts.
2. **Word-boundary/whole-token matching applied from day one, specifically
   because six prior disclosed limitations already proved the alternative
   fails.** `module_resolver.py` (basename equality) and
   `relevance_scorer.py` (tokenized set overlap, reusing
   `context-optimizer`'s ADR-019 technique) are both built correct from
   the first line of code — not patched in after a real dogfood run, the
   way `refactoring-safety`/`regression-hunter`/`release-readiness`'s
   `target_resolver.py` copies were. This is applying an *accumulated*
   lesson (L14/L19/L21/L23/L24/L28/L29/L30), not discovering a new one —
   and a real dogfood run still found a **different**, previously-
   theoretical residual gap the same day: see L31 in
   [[12-known-limitations]].
3. **Stays on the normal fail-closed-toward-caution side, not ADR-019's
   inversion.** A record flagged stale (a `FIXED`/`SUPERSEDED` title, or a
   mentioned module that no longer resolves against the current CI report)
   is still returned — never silently dropped, since an agent might judge
   it still relevant — but always with the flag attached, never presented
   as equivalent to an unflagged, `ACTIVE` record. This is the direct,
   operational answer to A8's own named risk in
   [[16-assumptions-and-validation]]: "stale/unvalidated memory could
   actively degrade performance if treated as authoritative."

A real dogfood run (`examples/engineering-memory/example-run.md`) against
this project's own actual 50-record memory bank (20 decisions, 30
limitations) found both staleness paths firing correctly on real data (a
real `FIXED` title, a real missing-module mention) — and surfaced a new,
concrete finding: `module_resolver.py`'s basename-exact resolution
collapses every record mentioning a basename shared across many skills
(`ci_report_loader.py` exists in most composing skills) into whichever
single real file the CI report lists last for that basename, regardless
of which skill's file the record actually names. Logged as **L31**,
disclosed not fixed — the substring-collision class this resolver was
built to defeat from day one is a genuinely different failure mode than
this one, and building the first correctly does not imply the second is
also solved.

- User Value: closes a gap `engineering-knowledge-capture` (Phase 12)
  named explicitly in its own Known Limitations — "the engine has no
  access to the memory bank's actual contents" — by going the opposite
  direction (task → retrieved existing entries, not narrative → candidate
  new entries), the natural complement rather than a duplicate skill.
- Correctness: every match traces to a real `record_id` and
  `source_file:source_line`; staleness is always computed and attached,
  never silently omitted for an ACTIVE-looking record.
- Security: read-only against the CI report and memory-bank files; never
  writes into `project-memory-bank/` itself; no network access.
- Simplicity: reuses Pattern 2 (ADR-007, FOURTEENTH reuse) and ADR-010
  (eleventh reuse) rather than inventing new architecture; corpus is
  deliberately limited to 2 files this pass, not a general-purpose
  markdown indexer.
- Maintainability: engine files land under 300 lines each (max
  `memory_bank_parser.py` at 148 lines), consistent with this project's
  <300-line-per-file discipline, restated explicitly by the user when
  directing this phase.
- Portability: no cross-skill Python imports — `keyword_extractor.py` is
  independently duplicated from `context-optimizer`'s, the same boundary
  convention every prior composing skill's `ci_report_loader.py`-style
  copy already established.
- Evidence: L8 applies a FOURTEENTH time (self-authored, single-rater
  judgment-layer evaluation, perfect scores on all 8 fixtures — see
  [[12-known-limitations]]); building this skill does not move A8 off
  `UNKNOWN` — it creates the retrieval capability A8 would need to be
  tested against, nothing more (see Status below).
- Future Evolution: L31's real-dogfood finding is a genuinely new,
  disclosed residual gap distinct from the substring-collision class this
  resolver was already built to defeat — a future version could
  disambiguate same-basename mentions using the record's own
  `source_file` path proximity to the mentioned module, not attempted
  here.

**Status**: Adopted. Note on process: this phase was started at the
user's explicit direction on 2026-08-26, reopening the roadmap freeze a
FIFTH time (Phase 11 through Phase 14 were the first four reopenings) —
but unlike Phase 14, this reopening did **not** override a named,
phase-specific "do not build" decision: A8's own gating condition
("design only when reached") is satisfied, since Phase 15 is being
reached in its designated order. The **general** freeze (A2/A5 both
`UNKNOWN`, zero real external users) is still overridden by explicit user
direction, not satisfied. A2, A5, and A8 all remain `UNKNOWN`; starting
this phase is not new external-validation evidence for any of them and is
not presented as such. This is now deferred across five consecutive phase
boundaries. Completing this phase also completes the originally-scoped
15-skill portfolio named in [[08-roadmap]] — no Phase 16 exists in that
list; anything past this point is a newly-proposed scope, not "the next
phase," unless and until real external validation evidence changes A2/A5.
