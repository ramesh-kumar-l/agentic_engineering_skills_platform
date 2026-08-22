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
