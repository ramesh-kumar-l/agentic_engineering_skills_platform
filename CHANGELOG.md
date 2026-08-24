# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

- Phase 10: Release Readiness — tenth skill, the final skill in the
  Engineering Lifecycle group (`skills/release-readiness/`): `SKILL.md`
  contract reusing Pattern 2 (ADR-007) a ninth time — a deterministic
  engine (16 modules, each under 300 lines, max 211, 78 passing tests
  including a CLI test file written from the start) that parses a unified
  git diff (independent copy of `regression-hunter`'s/`adversarial-diff-
  reviewer`'s parsing conventions), scans it for four mechanically-
  detectable, release-blocking diff-hygiene shapes (debug leftovers,
  merge-conflict markers, hardcoded-secret-shaped literals, TODO-blocking
  markers), resolves each changed file against `codebase-intelligence`'s
  real modules (a third independent copy of the `target_resolver.py`
  pattern), checks an independently-computed test-coverage signal, and
  combines these three always-available axes into a per-file
  `readiness_tier` via a documented rule table — plus OPTIONALLY loads and
  surfaces (never re-derives) evidence from a supplied `regression-hunter`
  and/or `security-context-guard` report — combined with an agent-driven
  Release Readiness Checklist workflow (a ninth checklist in
  `project-memory-bank/05-evaluation-framework.md`, the first with a
  non-negotiable advisory-only framing category); an 8-fixture evaluation
  harness (`evaluations/release-readiness/`, all 8 scored perfect on both
  layers, two fixtures deliberately exercising real axis divergence); and
  a dogfood run (`examples/release-readiness/`) that regenerated a fresh
  `codebase-intelligence` report against this repo's current 10-skill
  state and assessed a real, staged-then-unstaged (never committed) `git
  diff` of this phase's own 78 new files, confirming a predicted
  false-positive shape concretely (a legitimate CLI `print()` flagged as a
  debug leftover) and disclosing — without fixing — a sharper, more
  consequential version of the L14/L19/L21/L23 limitation class (L24):
  `target_resolver.py`'s substring-based resolution, reused a third time,
  produces false-positive TEST COVERAGE, not just an inflated caller list.
  New architectural decision — **ADR-016**: the Release Readiness
  Scorecard combines three always-available, non-blended axes into a
  per-file tier and rolls per-file tiers into one advisory-only overall
  verdict; two further, optional, cross-skill-composed axes are surfaced
  but deliberately never blended in. Reuses `feature-planner`'s,
  `root-cause-analyzer`'s, `architecture-decision`'s, `refactoring-
  safety`'s, and `regression-hunter`'s mandatory-composition rule
  (ADR-010) a sixth time, and `security-context-guard`'s optional-
  composition precedent (ADR-011) for the two new optional axes
  specifically — both stated explicitly as reuses.

- Phase 9: Regression Hunter — ninth skill
  (`skills/regression-hunter/`): `SKILL.md` contract reusing Pattern 2
  (ADR-007) an eighth time — a deterministic engine (11 modules, each under
  300 lines, max 181, 64 passing tests including a CLI test file written
  from the start) that parses a unified git diff into structured per-file
  hunks (an independent copy of `adversarial-diff-reviewer`'s parsing
  conventions), scans those hunks for mechanically-detectable regression
  patterns (removed exception handling, removed conditional guards,
  decreased test assertions, large deletions, modified signatures with no
  matching test-file change), resolves each changed file against
  `codebase-intelligence`'s real modules for structural blast radius, and
  checks an independently-computed test-coverage signal — combined into an
  overall per-file risk tier via an agent-driven Regression Risk Checklist
  workflow (an eighth checklist in
  `project-memory-bank/05-evaluation-framework.md`); an 8-fixture
  evaluation harness (`evaluations/regression-hunter/`, all 8 scored
  perfect on both layers); and a dogfood run
  (`examples/regression-hunter/`) that regenerated a fresh
  `codebase-intelligence` report against this repo's current 9-skill state
  and assessed a real, already-tested `codebase-intelligence` fix this
  phase's own build produced (excluding `*.egg-info` directories from repo
  scans), disclosing — without fixing — a new limitation (L23):
  `target_resolver.py`'s substring-based caller matching produces a wildly
  inflated caller list for short, common module stems, the same limitation
  class as L14/L19/L21 now shown to affect two skills' independent copies
  of the same heuristic simultaneously. New architectural decision —
  **ADR-015**: regression risk is scored from three explicit, non-blended
  signals per changed file (diff-pattern flags, structural blast radius,
  test-coverage status) combined via a documented rule table into an
  overall tier, with all three axes still visible separately. Reuses
  `feature-planner`'s, `root-cause-analyzer`'s, `architecture-decision`'s,
  and `refactoring-safety`'s mandatory-composition rule (ADR-010) a fifth
  time, stated explicitly as a reuse.

- Phase 8: Refactoring Safety — eighth skill
  (`skills/refactoring-safety/`): `SKILL.md` contract reusing Pattern 2
  (ADR-007) a seventh time — a deterministic engine (12 modules, each under
  300 lines, 62 passing tests including a CLI test file written from the
  start) that parses a refactoring description into an operation type
  (rename/delete/move/change-signature/split/merge/extract/inline, or a
  generic "refactor" fallback) and target identifiers (quoted/backticked
  first, bare-identifier fallback second), resolves each target against
  `codebase-intelligence`'s real modules, finds its real callers via an
  independent import scan, checks an independently-computed test-coverage
  signal, and scores a per-target risk tier from operation type and real
  fan-in/hotspot data — combined with an agent-driven Refactoring Safety
  Checklist workflow (10 categories, a seventh checklist in
  `project-memory-bank/05-evaluation-framework.md`); an 8-fixture
  evaluation harness (`evaluations/refactoring-safety/`, all 8 scored
  perfect on both layers); and a dogfood run
  (`examples/refactoring-safety/`) that regenerated a fresh
  `codebase-intelligence` report against this repo's current 8-skill state
  and assessed a real refactor this phase's own build actually produced (a
  duplicated path-stem helper across two of this skill's own modules),
  disclosing — without fixing — a new cross-skill limitation: `codebase-
  intelligence`'s own `fan_in` metric undercounted a real caller that this
  skill's own independent caller scan found correctly. New architectural
  decision — **ADR-014**: each target's risk tier is kept as a field
  distinct from an independently-computed test-coverage signal, rather than
  blended into one score. Reuses `feature-planner`'s, `root-cause-
  analyzer`'s, and `architecture-decision`'s mandatory-composition rule
  (ADR-010) a fourth time, stated explicitly as a reuse. Also clarifies an
  instruction discrepancy: the initial Phase 8 instruction named
  "Architecture Decision," already built as Phase 7 the prior session —
  confirmed with the user before work began that the actual intent was the
  roadmap's next proposed skill, Refactoring Safety.
- Phase 7: Architecture Decision — seventh skill
  (`skills/architecture-decision/`): `SKILL.md` contract reusing Pattern 2
  (ADR-007) a sixth time — a deterministic engine (11 modules, each under
  300 lines, 34 passing tests including a CLI test file written from the
  start) that parses a decision description into distinct options
  (explicit `Option A:` markers, numbered/lettered lists, or a
  `vs`/`versus` fallback split), then scores each option's structural
  blast radius against `codebase-intelligence`'s real dependency graph,
  rolling keyword relevance up into a `low`/`medium`/`high` tier driven by
  real fan-in and hotspot data — combined with an agent-driven
  Architecture Decision Record checklist workflow (10 categories, a sixth
  checklist in `project-memory-bank/05-evaluation-framework.md`); an
  8-fixture evaluation harness (`evaluations/architecture-decision/`, all
  8 scored perfect on both layers); and a dogfood run
  (`examples/architecture-decision/`) that regenerated a fresh
  `codebase-intelligence` report against this repo's current 7-skill state
  and assessed a real decision this phase's own build actually faced
  (required vs. optional composition), finding and fixing a real gap in
  the tradeoff-detection regex same-session (a verb-phrasing miss) and
  separately disclosing — without fixing — a sharper version of the
  coincidental-keyword-match limitation at full-repository scale. New
  architectural decision — **ADR-013**: each option's blast radius is
  scored in a three-tier structural-risk band from real fan-in/hotspot
  data rather than a bare relevance number. Reuses `feature-planner`'s and
  `root-cause-analyzer`'s mandatory-composition rule (ADR-010) a third
  time, stated explicitly as a reuse. Also corrects a phase-ordering
  discrepancy: the roadmap had proposed Refactoring Safety for Phase 7;
  this phase's actual instruction named Architecture Decision instead, so
  Refactoring Safety now sits at Phase 8 (`project-memory-bank/
  08-roadmap.md`).
- Phase 6: Root Cause Analyzer — sixth skill
  (`skills/root-cause-analyzer/`): `SKILL.md` contract reusing Pattern 2
  (ADR-007) a fifth time — a deterministic engine (11 modules, each under
  300 lines, 32 passing tests including a CLI test file written from the
  start) that parses a symptom description, optionally extracts stack-trace
  frames (Python tracebacks + generic `path:line`), and scores
  `codebase-intelligence` modules as candidate root-cause locations in two
  explicit, non-blended evidence tiers (`stack-trace` vs. `keyword`) —
  combined with an agent-driven Root Cause Investigation Checklist workflow
  (10 categories, a fifth checklist in
  `project-memory-bank/05-evaluation-framework.md`); an 8-fixture
  evaluation harness (`evaluations/root-cause-analyzer/`); and a dogfood
  run (`examples/root-cause-analyzer/`) that regenerated a fresh
  `codebase-intelligence` report against this repo's current 6-skill state
  and retrospectively diagnosed a natural-language description of Phase
  5's own L16 defect, ranking the true root-cause file first out of 122
  scored modules. New architectural decision — **ADR-012**: candidate
  locations are scored in two explicit evidence tiers rather than one
  blended score, so a stack-trace-confirmed location is never presented
  with the same confidence as a coincidental keyword match. Reuses
  `feature-planner`'s mandatory-composition rule (ADR-010) a second time,
  stated explicitly as a reuse rather than a new decision. This phase also
  produced this project's first non-perfect judgment-layer evaluation score
  (case-03: 0.67/0.67 precision/recall, `project-memory-bank/
  12-known-limitations.md` L19), disclosed as-is rather than adjusted.
- Documentation & developer-experience pass (post-Phase-5, not a phase):
  root `requirements.txt` and `DEPENDENCIES.md` making the project's
  zero-runtime-dependency footprint explicit; `QuickStarterGuide.md`, a
  full first-run walkthrough; a fully rewritten, production-grade root
  `README.md` (architecture diagrams, an explicit evaluation-honesty
  section, a table of real bugs found via dogfooding); a 5-post public
  blog series under `blogs/` (contract model, the two architecture
  patterns, the five real dogfooding bugs, the self-graded-evaluation
  trap, and the security model's advisory-only design), each verified
  against real code/data before writing; and a `**Status**` line added to
  each of the five skills' own `README.md`. No code, tests, `SKILL.md`
  contracts, or evaluation results changed — documentation only.
- Phase 5: Security Context Guard — fifth skill
  (`skills/security-context-guard/`): `SKILL.md` contract reusing Pattern 2
  (ADR-007) a fourth time — a deterministic classify/minimize/sanitize
  engine (12 modules, each under 300 lines, 58 passing tests including a
  CLI test file written from the start) covering secret/PII/sensitive-path/
  high-risk-action pattern matching with in-place redaction, combined with
  an agent-driven Security Decision Checklist workflow (7 categories, a
  fourth checklist in `project-memory-bank/05-evaluation-framework.md`,
  shaped as a decision-gate rather than a coverage-enumeration list); an
  8-fixture evaluation harness scoring both layers
  (`evaluations/security-context-guard/`); and a dogfood run
  (`examples/security-context-guard/`) against this phase's own real source
  and a real pending git-push decision this session actually faced. New
  architectural decision — **ADR-011**: the engine's recommendation is
  always advisory — it classifies and recommends, never authorizes an
  action itself, extending ADR-008's redact-not-exclude discipline from
  diff-content secrets to a general classify/minimize/sanitize surface.
  Composition with `codebase-intelligence` stays optional here, unlike
  ADR-010. The dogfood run found and fixed a real bug in the skill's own
  action classifier (a fixed-distance proximity window that real phrasing
  exceeded by 150+ characters, replaced with same-sentence co-occurrence
  matching — `project-memory-bank/12-known-limitations.md` L16), and
  doubled as Pilot C, the first internal pilot toward Assumption A7 (does
  security handling increase trust) in
  `project-memory-bank/17-experiment-viability-check.md`.
- Phase 4: Feature Planner — fourth skill (`skills/feature-planner/`):
  `SKILL.md` contract reusing Pattern 2 (ADR-007) a third time — a
  deterministic relevance-scoring/planning-flag engine (11 modules, each
  under 300 lines, 21 passing tests) combined with an agent-driven
  structured-plan-derivation workflow against a new 10-category Plan
  Quality checklist (`project-memory-bank/05-evaluation-framework.md`); an
  8-fixture evaluation harness scoring both layers
  (`evaluations/feature-planner/`); and a dogfood run
  (`examples/feature-planner/`) against a freshly regenerated
  `codebase-intelligence` report of this repo's own current (4-skill)
  state, using a real task. New architectural decision — **ADR-010**: this
  is the first skill where composing on `codebase-intelligence`'s output is
  a hard precondition, not optional context; the engine refuses to run
  without a valid report. The dogfood run found and fixed a real gap
  (`skills/acceptance-test-engineer/engine/cli.py` had zero test coverage —
  `skills/acceptance-test-engineer/tests/test_cli.py`, 4 new tests, the
  second cross-skill dogfood finding) and documented a real, deliberately
  unfixed relevance-ranking limitation (`project-memory-bank/12-known-
  limitations.md` L14) with concrete evidence the agent's judgment
  compensates for it in practice.
- Phase 3: Acceptance Test Engineer — third skill
  (`skills/acceptance-test-engineer/`): `SKILL.md` contract reusing Pattern 2
  (ADR-007) — a deterministic testability-anti-pattern engine (9 modules,
  each under 300 lines, 20 passing tests) combined with an agent-driven
  acceptance-case-derivation workflow against a new 10-category
  acceptance-coverage checklist (`project-memory-bank/05-evaluation-
  framework.md`); an 8-fixture evaluation harness scoring both layers
  (`evaluations/acceptance-test-engineer/`); and a dogfood run against a
  real, already-shipped requirement (`examples/acceptance-test-engineer/`)
  that found and fixed a real gap — `adversarial-diff-reviewer`'s CLI had
  zero test coverage (`skills/adversarial-diff-reviewer/tests/test_cli.py`,
  4 new tests, first cross-skill dogfood finding).
- `project-memory-bank/17-experiment-viability-check.md` — a first,
  explicitly-labeled viability check for the product thesis's Experiment
  A/B, including two N=1 internal pilots, governed by new ADR-009 (pilots
  must never be presented as the validated experiment).
- Phase 2: Adversarial Diff Reviewer — second skill
  (`skills/adversarial-diff-reviewer/`): `SKILL.md` contract combining a
  deterministic risk-flagging engine (9 modules, each under 300 lines, 19
  passing tests) with an agent-driven adversarial review workflow, an
  8-fixture evaluation harness scoring both the deterministic layer
  (automated) and a judgment layer (this session's agent actually performing
  each review — `evaluations/adversarial-diff-reviewer/`), and a dogfood run
  against a real in-session diff (`examples/adversarial-diff-reviewer/`) that
  found and fixed two real secret-redaction bugs in sequence.
- ADR-007 (deterministic pre-processor + agent-driven adversarial workflow
  pattern) and ADR-008 (redact-not-exclude for secrets in diff content) in
  `project-memory-bank/11-decisions.md`.
- Phase 1: Codebase Intelligence — first real skill
  (`skills/codebase-intelligence/`): `SKILL.md` contract, stdlib-only Python
  engine (11 modules, each under 300 lines, 23 passing tests), a 4-fixture
  evaluation harness (`evaluations/codebase-intelligence/`, all passing), and
  a dogfood run against this repo (`examples/codebase-intelligence/`) that
  found and fixed a real false-positive entry-point detection bug.
- New memory-bank files: `03-architecture.md`, `12-known-limitations.md`,
  `implementation-status.md`, `active-context.md`.
- ADR-005 (SKILL.md + deterministic engine pattern) and ADR-006 (stdlib-only
  Python engine choice) in `project-memory-bank/11-decisions.md`.
- Phase 0: Foundation — established `project-memory-bank/` (project vision,
  product thesis, requirements, skill contract, evaluation framework, security
  model, current-state tracking, roadmap, architectural decisions, assumptions
  ledger, and Sprint 00 record).
- Repository scaffolding: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`,
  `ROADMAP.md`.

No skill has been used on real (non-synthetic, non-agent) engineering work yet.
