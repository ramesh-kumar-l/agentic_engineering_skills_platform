# 18 — Test Engineering Platform: Product Contract

This file defines the **Product Contract** for the newly-proposed pivot
logged as [[11-decisions|ADR-023]] — the master system prompt's own Phase 1
deliverable, executed at the user's explicit direction on 2026-09-06.

**Naming note**: this file's "TEP Phase N" numbering belongs to the master
prompt's own 19-phase sequence (its section 36), and is **unrelated** to
this repo's own completed Phase 1–15 skill-portfolio roadmap in
[[08-roadmap]] (closed at Phase 15, no Phase 16 — see ADR-021). "TEP Phase
1" below means "the master prompt's Phase 1," never this repo's own Phase
1 (`codebase-intelligence`). Kept prefixed throughout to avoid the
collision.

## Mission

Evolve the 15-skill Agentic Engineering Skills Platform from a portfolio of
independent analysis/advisory skills into a **project-aware test
engineering capability**: given a staged code change, help an engineer
produce the smallest set of high-value, project-conformant regression tests
with high confidence — validated independently, not self-certified.

## Problem

Today's portfolio (`regression-hunter`, `refactoring-safety`,
`release-readiness`) already flags *risk* in a change with real structural
data. None of the fifteen skills *generates* a test, *executes* it, or
measures whether it actually protects the changed behavior. "Coverage" in
every skill that checks it today means "a test-shaped file imports this
module" — a static-import heuristic, not evidence a test runs or passes
(confirmed in Phase 0's audit).

## Target user

The same engineer this platform already targets (per [[01-product-thesis]]):
someone reviewing or authoring a code change who wants regression protection
without writing every test by hand — extended here to explicitly include
Java/Kotlin/Android engineers, since that is this pivot's headline new
surface.

## Job-to-be-done

Unchanged from [[01-product-thesis]]'s framing, narrowed: **given a staged
diff, determine which changed behaviors need a regression test, generate
one that matches the target project's real conventions, and prove — not
assert — that it compiles/runs and exercises the change.**

## Product thesis (restated against real Phase 0 findings, not assumed)

The master prompt's thesis — deterministic tooling verifies what can be
verified, AI reasons about what should be tested, evidence determines
trust — is **directly continuous** with this project's own standing
architecture: ADR-005/007's deterministic-engine-plus-agent-judgment split
already implements exactly this separation for every one of the 15
existing skills. This pivot does not introduce a new architectural
philosophy; it applies the existing one to a new output type (a generated,
executed test) instead of an analysis report.

## Scope for TEP Phase 2 onward (not yet started — see exit criteria below)

- Reuse `codebase-intelligence`'s report as the structural substrate for
  target resolution (same ADR-010 required-composition pattern this
  portfolio already applies 11 times).
- Extend, not replace, `regression-hunter`'s and `refactoring-safety`'s
  existing risk signals to select *which* changed behavior needs a test —
  do not build a second, competing risk scorer.
- Java/Kotlin source-level support already exists (ADR-022); Android
  framework support (JUnit, Mockito, Robolectric, Espresso, AGP, source
  sets/variants) is genuinely new build, not an extension of anything that
  exists today.

## Non-goals (explicit, per this project's standing anti-scope-creep discipline)

- No IDE plugin, hosted service, or UI — same boundary [[02-requirements]]
  already sets, unchanged.
- No live network calls (CVE databases, package registries, emulator
  provisioning services) — continues ADR-006's offline, stdlib-only default
  unless a specific later phase makes an explicit, evidence-backed
  exception (e.g., a local emulator invocation is execution, not a network
  call, and would need its own security review per [[06-security-model]]).
- No claim that a generated test is "verified useful" below Trust Ladder
  Level 4 (mutation evidence) — reuses this project's NFR4 (no unsupported
  reliability claims) applied to the master prompt's own Trust Ladder.
- No mutation testing tool, coverage tool, or Android emulator integration
  is scoped into TEP Phase 2 — each is a real, separate build with its own
  exit criteria (see below); none is assumed solved by defining this
  contract.

## Current maturity (Phase 0 findings, restated here as the honest starting line)

- Deterministic/AI-split architecture: **exists**, reusable as-is.
- Structural project intelligence (`codebase-intelligence`): **exists**,
  Java/Kotlin source-level (ADR-022), Android-framework-level absent.
- Risk signals for "what changed / what's risky": **exists**
  (`regression-hunter`, `refactoring-safety`).
- Test *generation*: **does not exist** anywhere in the portfolio.
- Independent *validation* (compile/execute/mutation): **does not exist**.
- Evidence/provenance schema (model/prompt version, run identity): **does
  not exist** — `evaluations/<skill>/actual+expected` JSON is evidence of a
  *skill's own* correctness, not of a *generated test's* usefulness.

## North-star metric (proposed only — zero real measurements exist yet)

Adopting the master prompt's **Verified Useful Test Rate** concept as the
target metric for this pivot, explicitly flagged the same way
[[16-assumptions-and-validation]] flags every unproven assumption in this
project: proposed, not measured, and not to be cited as evidence of
anything until a real generation+validation pipeline exists to measure it
against.

## TEP phase sequence and exit criteria

Only phases with enough real information to scope are defined now — later
ones are intentionally left undefined per this project's standing
anti-speculation discipline (ADR-006, ADR-009): designing Phase 6 in detail
before Phase 2 ships would be exactly the kind of premature architecture
this project has repeatedly declined to do.

- **TEP Phase 2 — Evidence Foundation.** Exit criteria: a run-provenance
  schema (repo/commit/skill-version/model/prompt-version/timestamp) is
  defined in a new memory file and demonstrated on at least one real,
  non-fixture run of an existing skill (not a new skill) before any new
  code is written for test generation itself.
- **TEP Phase 3 — Project Intelligence extensions.** Exit criteria: a
  `TestEnvironmentProfile`-equivalent (language, build system, test
  framework, mocking framework, coverage tool availability) is derived from
  a real target repo and cross-checked against `codebase-intelligence`'s
  existing `external_dependencies` output, reusing it rather than
  re-parsing manifests a second time.
- **TEP Phase 4 — Test Environment Discovery (Android/JVM specifically).**
  Exit criteria: the profile above correctly identifies JUnit/Robolectric/
  Espresso presence (or absence) on at least one real open-source
  Android repo, and explicitly reports "unavailable," never a guess, when a
  framework isn't detected.
- **TEP Phase 5 and beyond** (Test Strategy Engine, Scenario Planner, Test
  Generation, Independent Validation, Human Review, Engineering Memory
  extension, Evaluation/Ablation, external validation, DX, security/
  production hardening, public distribution) are named in the master
  prompt's own section 36 list but **not scoped here** — each requires its
  own Phase Execution Contract pass (read memory, define objective, define
  exit criteria) at the time it is actually started, per the master
  prompt's own section 38 and this project's own phase-by-phase discipline.

## Constraints carried over unchanged from the existing platform

- Strict modularity: engine files stay under 300 lines — an existing
  convention (stated explicitly across ADR-005 through ADR-022), not new to
  this pivot; the file-size rationale (token cost of reading a file the
  agent doesn't need) applies identically to any new TEP engine code.
- Memory-bank-first: `implementation-status.md` and `active-context.md`
  are updated at the end of every major feature, continuing this file
  header's own standing rule, unchanged.
- ADR-per-major-decision, disclose-don't-hide limitations, evidence before
  marketing claims (NFR4) — all unchanged, all apply to TEP work
  identically to every prior phase's work.

## Status

TEP Phase 1 (this contract) is complete as of 2026-09-06, per the user's
explicit direction to continue past TEP Phase 0.

TEP Phase 2 (Evidence Foundation) is also complete as of 2026-09-06, per
the user's explicit direction to continue past TEP Phase 1. Implemented as
the new `evidence/` package — see [[19-evidence-provenance-schema]] and
[[11-decisions|ADR-024]] for the schema and implementation decision, and
`examples/evidence/example-run.md` for the real, non-fixture demonstration
this phase's exit criteria required.

TEP Phase 3 (Project Intelligence extensions) has **not** started — per
the master prompt's own hard-stop rule (section 39) and this project's own
phase-by-phase discipline, it requires a new, separate, explicit user
instruction, not automatic continuation from this contract's completion.
