# 07 — Current State

**The most important file for implementation context.** This file describes ONLY
what currently exists — it is replaced/updated each phase, not appended to.
Read this before any other memory file when starting new work. For finer-grained
"what's in flight" detail, see [[active-context.md]] and [[implementation-status.md]].

_Last updated: 2026-08-23 — end of Phase 2._

## Repository contents

```
LICENSE                    Apache-2.0 (pre-existing, unmodified)
README.md                  Project overview, points to memory bank
CONTRIBUTING.md            How to propose a skill
SECURITY.md                Vulnerability reporting policy
ROADMAP.md                 Public pointer to 08-roadmap.md
CHANGELOG.md                Keep-a-Changelog format
project-memory-bank/       This memory bank (see below)
skills/codebase-intelligence/       Skill 1 — SKILL.md + Python engine
skills/adversarial-diff-reviewer/   Skill 2 — SKILL.md + Python engine + agent workflow
evaluations/codebase-intelligence/       Evaluation harness + 4 fixtures + RESULTS.md
evaluations/adversarial-diff-reviewer/   Evaluation harness + 8 fixtures + RESULTS.md
examples/codebase-intelligence/          Dogfood run against this repo itself
examples/adversarial-diff-reviewer/      Dogfood run against a real in-session diff
```

`workflows/` and `docs/` still do not exist — no composed workflows or
additional docs content yet.

## project-memory-bank/ contents

```
00-project-vision.md
01-product-thesis.md
02-requirements.md
03-architecture.md              updated this phase (Pattern 2 added)
04-skill-contract.md
05-evaluation-framework.md
06-security-model.md
07-current-state.md             (this file)
08-roadmap.md
11-decisions.md                 updated this phase (ADR-007/008)
12-known-limitations.md         updated this phase (L5-L9)
16-assumptions-and-validation.md   updated this phase (A2, A5)
implementation-status.md        updated this phase
active-context.md               updated this phase
sprint-history/SPRINT-00.md
sprint-history/SPRINT-01.md
sprint-history/SPRINT-02.md     NEW this phase
```

Still not created (deliberately): `09-workflow-catalog.md` (no composed
workflows yet), `10-ui-ux-principles.md` (no UI yet), `13-lessons-learned.md`,
`14-community-feedback.md`, `15-metrics.md` (no external usage yet).

## What exists in practice

- **Two skills implemented**, both Level 2 (Evaluated) per
  [[04-skill-contract]]'s maturity model, both Trust Status EXPERIMENTAL:
  - `codebase-intelligence` — fully deterministic (Pattern 1, ADR-005/006).
  - `adversarial-diff-reviewer` — deterministic risk-flagging engine +
    agent-driven adversarial review workflow (Pattern 2, ADR-007/008).
  Full detail in [[implementation-status.md]].
- **Two evaluation harnesses**: codebase-intelligence (4 fixtures, all
  passing) and adversarial-diff-reviewer (8 fixtures, deterministic layer
  100% correct, judgment layer 100% precision/recall — but see the caveat
  below).
- **42 total unit/integration tests** across both skills (23 + 19), all
  passing.
- **Three real bugs found and fixed via dogfooding**, not hypothetical:
  L1 (Phase 1, false-positive entry-point detection) and L5/L6 (Phase 2, two
  successive secret-redaction gaps, the second found by adversarially
  re-reviewing the fix for the first). See [[12-known-limitations]].
- **A methodological first**: Phase 2 is the first skill whose evaluation
  required an actual agent turn, not just deterministic code — the "Agent
  Runtime" step of [[05-evaluation-framework]]'s pipeline was exercised for
  real. But the same agent authored the fixtures, ground truth, AND the
  review — see L8. This is disclosed explicitly, not glossed over: the 100%
  judgment-layer score is evidence the workflow runs end-to-end, not evidence
  of real-world review quality.
- **Zero real-world usage by anyone other than this session's agent**, for
  either skill. Assumptions A2/A3/A5 have partial (synthetic, self-authored)
  evidence only — not real-world validation, not independent-rater
  validation.
- **Zero composed workflows, zero UI, zero product code beyond these two
  skills.**

## What Phase 2 established

A second architectural pattern (deterministic pre-processor + agent-driven
adversarial workflow, ADR-007) for skills where the task is judgment, not
structure extraction — the explicit counterpart to Phase 1's fully-
deterministic pattern. Also produced the project's first real evidence
(however preliminary) toward assumption A5's judgment-evaluation question,
and the first concrete instance of running an actual agent as the "Agent
Runtime" step in the evaluation pipeline described in
[[05-evaluation-framework]].

## Immediate next decision point

Phase 3 (`Acceptance Test Engineer`) is next per [[08-roadmap]], but has
**not** been started and requires explicit user go-ahead — per the
adaptive-roadmap rule, it must be re-justified against evidence at that time,
not assumed. See the Phase 2 completion report for the recommendation.
