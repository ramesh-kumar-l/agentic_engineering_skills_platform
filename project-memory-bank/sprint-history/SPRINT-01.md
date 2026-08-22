# Sprint 01 — Phase 1: Codebase Intelligence

## Goal
Build the first real skill end-to-end (contract + working engine + tests +
evaluation), reusable as an architectural reference for later skills.

## Hypothesis
A deterministic, stdlib-only Python engine wrapped in a SKILL.md contract is
buildable, testable, and evaluable within the platform's existing framework
(ADR-005/006).

## Success Criteria
Engine implemented with all modules <300 lines; tests pass; evaluation harness
runs against ≥3 fixtures with real scores; SKILL.md meets the canonical
template; memory bank updated per the user's "save state" requirement.

## Completed Work
`skills/codebase-intelligence/` (SKILL.md, engine, tests), 4-fixture evaluation
harness, dogfood run + bug fix, `project-memory-bank/03-architecture.md`,
`12-known-limitations.md`, `implementation-status.md`, `active-context.md`,
ADR-005/006, updated `07-current-state.md`, `08-roadmap.md`,
`16-assumptions-and-validation.md`, `CHANGELOG.md`, `README.md`, `ROADMAP.md`.

## Evidence
23/23 tests passing. 4/4 evaluation fixtures passing (Correctness/Completeness/
Efficiency, automated). One real bug found and fixed via dogfooding (L1 in
`12-known-limitations.md`). No real-world (non-synthetic, non-agent) usage yet.

## Evaluation
Automated dimensions (Correctness/Completeness/Efficiency) fully scored.
Safety/Relevance/Explainability intentionally left for human review, per
`05-evaluation-framework.md` — not scored by the model itself.

## Failures
L1 (false-positive entry-point detection via substring match) — found and
fixed within this sprint, not shipped. See `12-known-limitations.md`.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures under 10ms) and test/fixture pass rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-005 (SKILL.md + deterministic engine pattern), ADR-006 (stdlib-only
Python) — see `11-decisions.md`.

## Lessons Learned
Dogfooding on the platform's own repo caught a real correctness bug that
synthetic fixtures alone did not — worth doing before every phase closes, not
just this one.

## What We Should Stop / Continue / Change
- **Continue**: dogfood every skill against this repo before closing a phase.
- **Continue**: keep engine modules single-responsibility and under 300 lines.
- **Change**: consider a nested-manifest-aware `external_deps.py` once a
  second skill or real user hits the limitation (not preemptively — L2).

## Next Sprint Recommendation
Phase 2 (Adversarial Diff Reviewer), pending explicit user approval and
re-justification against evidence per the adaptive-roadmap rule.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular, tested, caught & fixed its own bug |
| Usefulness | 2 | Not yet used on real engineering work |
| Evaluation Quality | 3 | Automated dims solid; judgment dims untested |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, architecture, limitations all recorded |
| Focus | 5 | One skill, no scope creep into Phase 2+ |
| Learning | 4 | Dogfooding bug is a genuine, reusable lesson |
| Career Signal | 2 | Real artifact exists, but unvalidated by others |
