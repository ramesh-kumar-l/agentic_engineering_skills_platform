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
