# Changelog

All notable changes to this project are documented here. Format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added

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
