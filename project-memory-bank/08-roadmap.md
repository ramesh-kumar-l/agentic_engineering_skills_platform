# 08 — Roadmap

The roadmap is adaptive. At every phase boundary, ask: "Is this next skill still
justified by evidence?" If no, update this file — do not build a planned skill
just because it was planned earlier. See [[16-assumptions-and-validation]].

## Phase list

```
PHASE 0  — Foundation                        ← COMPLETE
PHASE 1  — Codebase Intelligence             ← COMPLETE
PHASE 2  — Adversarial Diff Reviewer         ← COMPLETE
PHASE 3  — Acceptance Test Engineer          ← COMPLETE
PHASE 4  — Feature Planner                   ← COMPLETE
PHASE 5  — Security Context Guard            ← COMPLETE
PHASE 6  — Root Cause Analyzer               ← COMPLETE
PHASE 7  — Architecture Decision             ← COMPLETE (this phase, reordered — see note below)
PHASE 8  — Refactoring Safety                 ← proposed next, not started
PHASE 9  — Regression Hunter
PHASE 10 — Release Readiness
PHASE 11 — Dependency / Supply Chain
PHASE 12 — Knowledge Capture
PHASE 13 — Context Optimizer
PHASE 14 — Workflow Composer
PHASE 15 — Engineering Memory
```

Each phase ends with a completion report and a hard STOP for user instruction
(Section 39–40 of the operating charter). No phase auto-continues into the next.

## Full target skill portfolio (do not build all at once)

**Foundation**: codebase-intelligence, feature-planner, acceptance-test-engineer,
adversarial-diff-reviewer, security-context-guard.

**Engineering Lifecycle**: root-cause-analyzer, refactoring-safety,
architecture-decision, regression-hunter, release-readiness.

**Advanced**: dependency-supply-chain-reviewer, engineering-knowledge-capture,
context-optimizer, workflow-composer, engineering-memory.

First milestone is 3 genuinely useful, evaluated skills used on real work — not
all 15.

## First-five ordering decision

Chosen order: **Codebase Intelligence → Adversarial Diff Reviewer →
Acceptance Test Engineer → Feature Planner → Security Context Guard**, rather
than the original catalog order.

Rationale: the first three let the core thesis be tested fast —
`UNDERSTAND → VERIFY → DEFINE CORRECTNESS` — before any orchestration or planning
investment. Feature Planner then extends this to
`UNDERSTAND → PLAN → DEFINE → IMPLEMENT → VERIFY`, giving a stronger
experimental foundation before memory, registry, or UI work. Logged formally in
[[11-decisions]].

## Phase 0 scope

Repository structure, memory bank, skill contract, evaluation framework,
assumptions ledger, security model, roadmap, contribution model, tracking. No
skill implementation, no product functionality.

## Phase 1 scope (this phase) — complete

Built `codebase-intelligence`: `SKILL.md` contract + a stdlib-only Python
engine (11 modules, each under 300 lines) + 23 passing tests + a 4-fixture
evaluation harness (all passing) + a dogfood run against this repo that found
and fixed a real bug pre-ship. See [[03-architecture]],
[[implementation-status.md]], [[12-known-limitations]]. Established the
"SKILL.md + deterministic engine" pattern (ADR-005/006 in [[11-decisions]])
for reuse by later skills where the underlying task is deterministic.

No real-world (non-agent) usage yet — see [[16-assumptions-and-validation]]
for what Phase 1 did and did not validate.

## Phase 2 scope (this phase) — complete

Built `adversarial-diff-reviewer`: a second architectural pattern
(deterministic risk-flagging engine + agent-driven adversarial review
workflow, ADR-007/008 in [[11-decisions]]) for judgment-based skills, the
counterpart to Phase 1's fully-deterministic pattern. `SKILL.md` contract +
19 passing tests + an 8-fixture evaluation harness scoring both the
deterministic layer (automated) and the judgment layer (this session's agent
actually performing the review, not fabricated) + a dogfood run against a
real diff that found and fixed two real bugs in sequence (L5, L6 in
[[12-known-limitations]]). See [[03-architecture]] Pattern 2,
[[implementation-status.md]].

Important honesty note: the judgment-layer evaluation's 100% precision/recall
is self-authored, single-rater evidence (L8) — the same agent wrote the
fixtures, ground truth, and review. Do not read it as proof of real-world
review quality; see [[16-assumptions-and-validation]] A5.

## Phase 3 scope (this phase) — complete

Built `acceptance-test-engineer`, reusing Pattern 2 as-is (no new base-pattern
ADR) for a second judgment-based skill: `SKILL.md` contract + a deterministic
testability-anti-pattern engine + 20 passing tests + an 8-fixture evaluation
harness (same two-layer scoring and same up-front self-authored/single-rater
caveat as Phase 2) + a dogfood run against a real, already-shipped
requirement that found and fixed a real gap (L10 in [[12-known-limitations]]:
`adversarial-diff-reviewer`'s CLI had zero test coverage — the first
cross-skill dogfood finding).

Also delivered the exit criteria's second half: a first Experiment A/B
viability check, [[17-experiment-viability-check.md]] — assesses what's
missing to run either experiment for real, and runs two explicitly-labeled
internal pilots (N=1, self-run, not the real experiments) governed by new
ADR-009. Neither A2 nor A10 in [[16-assumptions-and-validation]] is upgraded
beyond what a single non-blinded pilot can support.

## Phase 4 scope (this phase) — complete

Built `feature-planner`, reusing Pattern 2 (ADR-007) a third time: `SKILL.md`
contract + a deterministic relevance-scoring/planning-flag engine + 21
passing tests + an 8-fixture evaluation harness (same two-layer scoring and
up-front self-authored/single-rater caveat as Phases 2-3, now applying a
third time) + a real dogfood run against this repo's own current state.

New this phase: ADR-010 — `feature-planner` is the first skill where
composition with `codebase-intelligence` is a **hard precondition**, not
optional context. The exit criteria's "first skill composing on top of
Codebase Intelligence's output" is implemented literally: the engine refuses
to run without a valid `report.json` (`engine/ci_report_loader.py`,
`CiReportError`). The real dogfood run
([[examples/feature-planner/example-run.md]]) regenerated a fresh
`codebase-intelligence` report against the repo's current (4-skill) state
and found two genuine things: (1) L13 — `acceptance-test-engineer`'s own CLI
had zero test coverage, the second cross-skill dogfood finding, fixed
same-session; (2) L14 — the relevance scorer's path-weighting floods when
task keywords collide with a shared directory name, a real limitation left
unfixed because the agent's Step 3 judgment is designed to (and did, in that
same run) correct for it — the strongest evidence yet that ADR-007's
two-layer split earns its complexity.

Important honesty note, carried forward from Phase 3: required composition
existing and working is evidence for a narrower claim ("composition
executes correctly and is genuinely used") than Experiment B requires
("composition measurably outperforms the individual-skill alternative,
against an independent baseline"). [[16-assumptions-and-validation]] A10
remains UNKNOWN — see ADR-009.

## Phase 5 scope (this phase) — complete

Built `security-context-guard`, reusing Pattern 2 (ADR-007) a fourth time:
`SKILL.md` contract + a deterministic classify/minimize/sanitize engine
(secret/PII/sensitive-path/action-category matching, in-place redaction) +
58 passing tests (including a CLI test file written from the start, not
discovered missing later) + an 8-fixture evaluation harness (same two-layer
scoring and up-front self-authored/single-rater caveat as Phases 2-4, now
applying a fourth time) + a real dogfood run against this phase's own real
source and a real pending git-push decision this session actually faced.

New this phase: ADR-011 — the engine's `suggested_verdict` is always
advisory; it classifies and recommends, never authorizes, per
[[06-security-model]]'s Human Approval principle. Unlike ADR-010,
composition with `codebase-intelligence` stays optional here. The real
dogfood run found and fixed a genuine bug in the skill's own action
classifier (L16 — a fixed-distance proximity window that real phrasing
exceeded, replaced with same-sentence co-occurrence matching) and doubled
as **Pilot C**, a first internal pilot toward
[[16-assumptions-and-validation]] A7 (does security handling increase
trust) — see [[17-experiment-viability-check]]. A7 stays UNKNOWN: the
pilot's one data point showed the structured report matched what this
session's existing bounded-autonomy behavior already produced on this case,
so it didn't yet demonstrate a changed decision — real qualitative feedback
from an actual user remains the missing ingredient, same shape as A2/A10's
gap.

## Phase 6 scope (this phase) — complete

Built `root-cause-analyzer`, reusing Pattern 2 (ADR-007) a fifth time and
`feature-planner`'s required-composition rule (ADR-010) a second time:
`SKILL.md` contract + a deterministic stack-trace/keyword tiered
candidate-location engine + 32 passing tests (CLI test file written from
the start, same discipline Phase 5 established) + an 8-fixture evaluation
harness (same two-layer scoring as Phases 2-5) + a real dogfood run
regenerating a fresh `codebase-intelligence` report against this repo's
current (6-skill) state and diagnosing a real, retrospective symptom.

New this phase: ADR-012 — candidate locations are scored in two explicit,
non-blended evidence tiers (`stack-trace`, a dominant flat bonus when a
parsed stack frame's path matches a real module, vs. `keyword`, the
fallback keyword-overlap tier) rather than one blended score, so the
agent's Step 3 investigation can always tell a runtime-confirmed location
apart from a vocabulary-coincidence lead. The exit criteria's "same bar" is
met: full engine/test/evaluation/dogfood/memory-bank cycle, same as every
prior phase; "first skill composing on top of Codebase Intelligence's
output" was already true of `feature-planner` (Phase 4, ADR-010) — this
phase reuses that same required-composition rule rather than re-claiming
the "first," and states that explicitly rather than overclaiming a novelty
that isn't there.

The real dogfood run (`examples/root-cause-analyzer/example-run.md`) fed a
natural-language description of Phase 5's own L16 defect — written without
naming the file or the fix — into the freshly-composed engine, which ranked
the module that actually contained that bug (`action_patterns.py`) first
out of 122 scored modules, using keyword-tier evidence alone (no stack
trace existed for that defect, since it was a silent misclassification).
Disclosed explicitly as retrospective validation, not a new bug find — a
prospective run against a genuinely new, not-yet-diagnosed symptom remains
unrun.

Important honesty note, carried forward from Phases 3-5: this is the
**fifth** judgment-based skill evaluated with self-authored, single-rater
fixtures — and the **first** whose judgment layer did not score perfect
precision/recall on every fixture (case-03 scored 0.67/0.67, disclosed
as-is — see L19 in [[12-known-limitations]]). [[16-assumptions-and-
validation]] A5 and A10 remain UNKNOWN; the inter-rater-agreement
experiment and Experiment B still have not been run.

## Phase 7 scope (this phase) — complete

Built `architecture-decision`, reusing Pattern 2 (ADR-007) a sixth time and
the required-composition rule (ADR-010, reused by `root-cause-analyzer`'s
ADR-012) a third time: `SKILL.md` contract + a deterministic option-parsing/
blast-radius-scoring engine + 34 passing tests (CLI test file written from
the start, same discipline every prior phase established) + an 8-fixture
evaluation harness (same two-layer scoring as Phases 2-6) + a real dogfood
run regenerating a fresh `codebase-intelligence` report against this repo's
current (7-skill) state and assessing a real decision this phase's own
build actually faced.

**Note on phase ordering**: this roadmap previously proposed Phase 7 as
Refactoring Safety, with Architecture Decision slotted at Phase 8 (see
`## Full target skill portfolio`). The user's Phase 7 instruction explicitly
named "Architecture Decision," not Refactoring Safety — this is a real
reordering, not a silent drift, so it's stated here plainly: Refactoring
Safety moves to Phase 8, Architecture Decision fills Phase 7. The
`## Full target skill portfolio` list below is left as the original catalog
ordering (unchanged) since the adaptive-roadmap rule already treats that
list as "do not build all at once," not a fixed sequence — the phase list
above is the authoritative record of what was actually built, in what
order.

New this phase: ADR-013 — each parsed option's structural blast radius is
scored against `codebase-intelligence`'s real fan-in/hotspot data, rolling
keyword relevance up into a three-tier band (`low`/`medium`/`high`) rather
than a bare relevance number, so a decision option that touches a real
hotspot is never presented with the same confidence as one that touches
nothing real. The exit criteria's "same bar" is met: full engine/test/
evaluation/dogfood/memory-bank cycle, same as every prior phase; "first
skill composing on top of Codebase Intelligence's output" was already true
of `feature-planner` (Phase 4) and reused by `root-cause-analyzer` (Phase
6) — this phase reuses that same required-composition rule a third time
rather than re-claiming the "first," the same honesty discipline Phase 6
applied to the identical phrasing.

The real dogfood run (`examples/architecture-decision/example-run.md`)
assessed a genuinely real decision — whether this skill itself should
require or merely accept `codebase-intelligence` composition — and found
two things worth stating plainly. First, a real, same-session-fixed bug:
the tradeoff-detection regex missed the verb phrasing "trades X for Y,"
which the dogfood decision's own text used twice (L20 in [[12-known-
limitations]]). Second, a real, disclosed-not-fixed limitation: at
full-repository scale, a decision *about the platform's own architecture*
produces a nearly-uninformative blast-radius signal, because the decision
text's vocabulary unavoidably overlaps the whole repo's own vocabulary
(L21). Unlike Phase 6, this phase's evaluation harness scored perfect
precision/recall on all 8 fixtures — stated plainly as not evidence of
higher judgment quality than Phase 6's non-perfect score, since a single
self-authored evaluation cannot support that comparison either way.

Important honesty note, carried forward from Phases 3-6: this is the
**sixth** judgment-based skill evaluated with self-authored, single-rater
fixtures. [[16-assumptions-and-validation]] A5 and A10 remain UNKNOWN; the
inter-rater-agreement experiment and Experiment B still have not been run —
now carried forward across six skills, not five.
