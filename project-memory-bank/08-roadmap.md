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
PHASE 7  — Architecture Decision             ← COMPLETE (reordered — see Phase 7 note below)
PHASE 8  — Refactoring Safety                 ← COMPLETE
PHASE 9  — Regression Hunter                  ← COMPLETE
PHASE 10 — Release Readiness                  ← COMPLETE
PHASE 11 — Dependency / Supply Chain          ← COMPLETE (this phase; started
                                                  at the user's explicit
                                                  direction, reopening a
                                                  same-day roadmap freeze —
                                                  not new validation evidence)
PHASE 12 — Knowledge Capture                  ← COMPLETE (started at the
                                                  user's explicit direction,
                                                  a SECOND same-day-freeze
                                                  reopening — not new
                                                  validation evidence)
PHASE 13 — Context Optimizer                  ← COMPLETE (this phase; started
                                                  at the user's explicit
                                                  direction, a THIRD
                                                  same-day-freeze reopening —
                                                  not new validation evidence)
PHASE 14 — Workflow Composer                  ← COMPLETE (this phase; started
                                                  at the user's explicit
                                                  direction, a FOURTH
                                                  same-day-freeze reopening,
                                                  the first to also override
                                                  A10 by name — not new
                                                  validation evidence)
PHASE 15 — Engineering Memory                  ← frozen, same as before Phase 14
```

Each phase ends with a completion report and a hard STOP for user instruction
(Section 39–40 of the operating charter). No phase auto-continues into the next.
Note (2026-08-26): the checked-in [[operating-charter]] contains no Section
39–40 — see [[12-known-limitations|L27]].

## Full target skill portfolio (do not build all at once)

**Foundation**: codebase-intelligence, feature-planner, acceptance-test-engineer,
adversarial-diff-reviewer, security-context-guard.

**Engineering Lifecycle**: root-cause-analyzer, refactoring-safety,
architecture-decision, regression-hunter, release-readiness.

**Advanced**: dependency-supply-chain-reviewer, engineering-knowledge-capture,
context-optimizer, workflow-composer, engineering-memory.

Naming drift (noted 2026-08-26): the shipped Phase 11 skill is
`dependency-supply-chain`, not `dependency-supply-chain-reviewer` as listed
in the original [[operating-charter]] §8 portfolio. Documented as drift, not
retroactively renamed.

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

## Phase 8 scope (this phase) — complete

Built `refactoring-safety`, reusing Pattern 2 (ADR-007) a seventh time and
the required-composition rule (ADR-010, reused by `root-cause-analyzer`'s
ADR-012 and `architecture-decision`'s ADR-013) a fourth time: `SKILL.md`
contract + a deterministic operation-parsing/target-resolution/risk-scoring
engine + 62 passing tests (CLI test file written from the start, same
discipline every prior phase established) + an 8-fixture evaluation
harness (same two-layer scoring as Phases 2-7) + a real dogfood run
regenerating a fresh `codebase-intelligence` report against this repo's
current (8-skill) state and assessing a real refactor this phase's own
build actually produced (a duplicated path-stem helper across two of this
skill's own engine modules).

**Note on the exit criteria's phrasing and phase naming**: the initial
instruction for this phase named "Architecture Decision" as Phase 8's exit
criteria — but `architecture-decision` was already built and completed as
Phase 7 the prior session. This discrepancy was surfaced and clarified with
the user before work began, who confirmed the actual intent was to build
this roadmap's next proposed skill, Refactoring Safety, rather than
re-building an already-complete skill. Stated here plainly rather than
silently building a duplicate `architecture-decision` under a new phase
number.

New this phase: ADR-014 — each resolved refactor target's structural risk
is scored into a three-tier band (`low`/`medium`/`high`) from real
fan-in/hotspot data (operation-type-aware: boundary-changing operations
like rename/delete/move/change-signature score against real fan-in;
internal-only operations like extract/inline score against hotspot status
alone), and a **separate**, independently-computed test-coverage signal
(does a real test-shaped module import the target) is checked against that
tier — the two are kept as distinct fields rather than blended, so a
structurally risky target with real test coverage is never confused with
one that has none. The exit criteria's "same bar" is met: full engine/test/
evaluation/dogfood/memory-bank cycle, same as every prior phase; composing
required on `codebase-intelligence`'s output was already true starting
Phase 4 — this phase reuses that same required-composition rule a fourth
time.

The real dogfood run (`examples/refactoring-safety/example-run.md`)
assessed a genuinely real refactor — extracting a path-stem helper
duplicated across this skill's own `target_resolver.py` and
`test_coverage_scanner.py` — and found one thing worth stating plainly: a
real, disclosed-not-fixed cross-skill limitation (L22 in [[12-known-
limitations]]) where `codebase-intelligence`'s own `fan_in` metric
undercounted a real caller (a test module using an absolute-style
cross-package import) that this skill's own independent caller scan found
correctly. Unlike Phase 7, all 8 evaluation fixtures scored perfect
precision/recall on both layers — stated plainly as not evidence of higher
judgment quality than Phase 6's non-perfect score, since a single
self-authored evaluation cannot support that comparison either way.

Important honesty note, carried forward from Phases 3-7: this is the
**seventh** judgment-based skill evaluated with self-authored, single-rater
fixtures. [[16-assumptions-and-validation]] A5 and A10 remain UNKNOWN; the
inter-rater-agreement experiment and Experiment B still have not been run —
now carried forward across seven skills, not six.

## Phase 9 scope (this phase) — complete

Built `regression-hunter`, reusing Pattern 2 (ADR-007) an eighth time and
the required-composition rule (ADR-010, reused by `root-cause-analyzer`'s
ADR-012, `architecture-decision`'s ADR-013, and `refactoring-safety`'s
ADR-014) a fifth time: `SKILL.md` contract + a deterministic diff-pattern/
structural-blast-radius/test-coverage engine + 64 passing tests (CLI test
file written from the start, same discipline every prior phase since Phase
5 established) + an 8-fixture evaluation harness (same two-layer scoring as
Phases 2-8) + a real dogfood run regenerating a fresh `codebase-
intelligence` report against this repo's current (9-skill) state and
assessing a real `git diff` this phase's own build actually produced (a
genuine `codebase-intelligence` scanner fix excluding `*.egg-info`
directories from repo scans).

New this phase: ADR-015 — given a git diff (not a free-text description,
unlike every prior composing skill), each changed file's regression risk is
computed as three explicitly separate, non-blended signals — diff-pattern
flags scanned directly against the diff's own hunks (Axis 1, the genuinely
new deterministic-layer contribution this phase, since no prior skill
scans a diff's hunks for mechanically-detectable regression shapes),
structural blast radius grounded in `codebase-intelligence`'s real fan-in/
hotspot data (Axis 2, reusing `refactoring-safety`'s `target_resolver.py`/
`safety_scorer.py` pattern as an independent copy), and test coverage
status (Axis 3, reusing `refactoring-safety`'s `test_coverage_scanner.py`
pattern as an independent copy) — combined into one `overall_risk_tier` per
file via a documented rule table, while all three underlying fields stay
visible and separately inspectable, never blended away. The exit criteria's
"same bar" is met: full engine/test/evaluation/dogfood/memory-bank cycle,
same as every prior phase; composing required on `codebase-intelligence`'s
output was already true starting Phase 4 — this phase reuses that same
required-composition rule a fifth time.

The real dogfood run (`examples/regression-hunter/example-run.md`)
assessed a genuinely real, already-tested change — a small
`codebase-intelligence` scanner fix (excluding `*.egg-info` directories
from repo scans) this phase's own build produced and fully tested (24/24
`codebase-intelligence` tests passing, up from 23) — and found one thing
worth stating plainly: a real, disclosed-not-fixed cross-skill limitation
(L23 in [[12-known-limitations]]) where `target_resolver.py`'s
substring-based caller-identification heuristic, present as an independent
copy in both `refactoring-safety` and `regression-hunter`, inflates the
caller list for any composed-report module whose stem is a short, common
word (e.g. `"scanner"` matching six other skills' own `*_scanner.py`
modules). Unlike Phase 6 (`root-cause-analyzer`'s one non-perfect
judgment-layer case), all 8 evaluation fixtures scored perfect precision/
recall on both layers here — stated plainly as not evidence of higher
judgment quality than Phase 6's non-perfect score, since a single
self-authored evaluation cannot support that comparison either way.

Important honesty note, carried forward from Phases 3-8: this is the
**eighth** judgment-based skill evaluated with self-authored, single-rater
fixtures. [[16-assumptions-and-validation]] A5 and A10 remain UNKNOWN; the
inter-rater-agreement experiment and Experiment B still have not been run —
now carried forward across eight skills, not seven.

## Phase 10 scope (this phase) — complete

Built `release-readiness`, the tenth skill and the final skill in the
Engineering Lifecycle group, reusing Pattern 2 (ADR-007) a ninth time and
the required-composition rule (ADR-010, reused by `root-cause-analyzer`'s
ADR-012, `architecture-decision`'s ADR-013, `refactoring-safety`'s ADR-014,
and `regression-hunter`'s ADR-015) a sixth time: `SKILL.md` contract + a
deterministic diff-hygiene/structural-blast-radius/test-coverage engine
(16 modules, each under 300 lines, max 211) that composes a git diff and a
required `codebase-intelligence` report into a per-file **Release Readiness
Scorecard**, plus optionally surfaces (never re-derives) evidence from a
`regression-hunter` and/or `security-context-guard` report for the same
change — 78 passing tests (CLI test file written from the start, same
discipline every prior phase since Phase 5 established) + an 8-fixture
evaluation harness (same two-layer scoring as Phases 2-9) + a real dogfood
run regenerating a fresh `codebase-intelligence` report against this
repo's current (10-skill) state and assessing this phase's own real body of
work via a real, staged-then-unstaged (never committed) `git diff`.

New this phase: **ADR-016** — the Release Readiness Scorecard combines
three always-available, non-blended per-file signals (diff-hygiene flags,
structural blast radius, test coverage) into a per-file `readiness_tier`
via a documented rule table, and surfaces two OPTIONAL, composed-elsewhere
signals (regression-hunter's `overall_risk_tier`, security-context-guard's
`suggested_verdict`) as distinct fields that deliberately do NOT feed that
rule table — reused/re-blended verdicts from a different skill's own
rule table would hide which skill produced which judgment, the same
"don't collapse the distinction away" discipline ADR-012/013/014/015
already established for their own axes. Per-file tiers roll up into one
`overall_verdict` (`NOT_READY`/`READY_WITH_CONDITIONS`/`READY`), explicitly
and repeatedly framed everywhere (SKILL.md, docstrings, README, this
section) as a recommendation for a human to review, never an autonomous
release gate — the same "advisory only" discipline ADR-011 established for
`security-context-guard`'s `suggested_verdict`, extended here to this
portfolio's highest-stakes recommendation. The exit criteria's "same bar"
is met: full engine/test/evaluation/dogfood/memory-bank cycle, same as
every prior phase; "first skill composing on top of Codebase
Intelligence's output" was already true of `feature-planner` (Phase 4) and
reused by five skills since — this phase reuses that same
required-composition rule a sixth time rather than re-claiming the
"first," the same honesty discipline every phase since Phase 6 has
applied to the identical phrasing.

The real dogfood run (`examples/release-readiness/example-run.md`)
assessed this phase's own actual body of work — a real, staged-then-
unstaged `git diff` of all 78 new `release-readiness` files (3,956 lines
added, 0 removed; nothing was ever committed) — and found two things worth
stating plainly. First, a real, confirmed instance of an
already-documented limitation: the `debug-print-leftover` hygiene pattern
fired 5 times on this skill's own `engine/cli.py` and
`evaluations/release-readiness/run_evaluation.py`, every one a legitimate
CLI `print()` call, not a debug leftover — `SKILL.md`'s Known Limitations
predicted this exact failure shape before the run; this run confirmed it
concretely rather than leaving it hypothetical, and it was left unfixed by
design (the documented boundary between the hygiene table and the agent's
Step 4 false-positive-check judgment). Second, a real, disclosed-not-fixed
limitation (L24 in [[12-known-limitations]]): `target_resolver.py`'s
substring-based resolution — a THIRD independent copy of the exact
heuristic already disclosed as L23 — was shown for the first time to
produce **false-positive test coverage**, not just an inflated caller
list, when a module's stem (e.g. `models`, `stats`, `report`) collides
with an identically-named module in an unrelated skill. This is a more
consequential manifestation than L23's caller-list-only inflation, since
it is the exact signal the readiness rule table uses to decide whether a
structurally consequential, genuinely untested module needs closer review.
Unlike most prior phases, this phase's evaluation harness scored perfect
precision/recall on all 8 fixtures — stated plainly as not evidence of
higher judgment quality than Phase 6's non-perfect score, since a single
self-authored evaluation cannot support that comparison either way.

Important honesty note, carried forward from Phases 3-9: this is the
**ninth** judgment-based skill evaluated with self-authored, single-rater
fixtures. [[16-assumptions-and-validation]] A5 and A10 remain UNKNOWN; the
inter-rater-agreement experiment and Experiment B still have not been run —
now carried forward across nine skills, not eight.

## Phase 11 — Dependency / Supply Chain (COMPLETE, 2026-08-26)

Per the roadmap's own phase list and full target skill portfolio
(`Advanced`: dependency-supply-chain-reviewer, engineering-knowledge-
capture, context-optimizer, workflow-composer, engineering-memory), Phase
11 was proposed as **Dependency / Supply Chain** — the first skill in the
`Advanced` group, now that all five Engineering Lifecycle skills exist.

**How this actually started**: earlier the same day, a mentor-review pass
froze the roadmap pending real external validation evidence (the
independent-evidence gap, L8/A5, and the four-times-disclosed L23/L24 bug
were the stated reasons) — Phase 11 was explicitly NOT going to auto-start.
The user then, in the same session, explicitly directed starting it anyway,
with their own stated exit criteria. That is a one-time, user-authorized
exception to the freeze, not evidence A2/A5 moved off `UNKNOWN` — recorded
here honestly rather than presented as if the freeze's conditions were met.
See [[11-decisions]] ADR-017 and [[active-context.md]] for the full build.

**What shipped**: `dependency-supply-chain` — pin-status, known-risk-name,
duplicate-version, and surface-area scanning, composing on a required
`codebase-intelligence` report (ADR-010, seventh reuse). 46 tests, 8/8
evaluation fixtures on both layers. Two scope decisions made explicitly
during the build rather than silently: no live CVE lookup (permanent,
L25), and no per-dependency license-risk detection (dropped mid-build once
it became clear the data doesn't exist in what's parsed — L26).

**Phase 12 onward**: the freeze from before Phase 11 remains in force. The
case for investing a phase in the independent-evidence gap (L8/A5) before a
twelfth skill, flagged as a growing concern since Sprint 08 and sharpened
by Sprint 09's L23 and Sprint 10's L24 (the substring-collision limitation
class, now fixed/partially-fixed — see [[12-known-limitations]]), remains
at least as strong as it was at the Phase 11 boundary — a future session
should weigh that explicitly before starting Phase 12, and should not read
Phase 11 shipping as precedent that the freeze auto-lifts on request alone
without the user again making that call explicitly.

## Phase 12 — Engineering Knowledge Capture (COMPLETE, 2026-08-26)

Per the roadmap's own phase list and full target skill portfolio
(`Advanced`: dependency-supply-chain-reviewer, engineering-knowledge-
capture, context-optimizer, workflow-composer, engineering-memory), Phase
12 was proposed as **Engineering Knowledge Capture** — the second skill in
the `Advanced` group.

**How this actually started**: exactly as predicted in the "Phase 12
onward" note directly above — the freeze from before Phase 11 was still in
force, and the case for investing in L8/A5 instead of a twelfth skill was
not weaker. The user then explicitly directed starting Phase 12 anyway,
with their own stated exit criteria (same shape as Phase 11's: "same bar,"
first skill composing on `codebase-intelligence`'s output — not literally
true, the eleventh Pattern 2 reuse and eighth ADR-010 reuse, stated plainly
in [[03-architecture]]/[[11-decisions]] — "scalable and production-level
stable"). This is a **second**, one-time, user-authorized exception to the
freeze, not evidence A2/A5 moved off `UNKNOWN` — recorded here honestly,
the same way Phase 11's exception was, rather than presented as if the
freeze's conditions were newly met.

**What shipped**: `engineering-knowledge-capture` — a deterministic
decision/lesson/limitation/workaround candidate scanner over a free-text
engineering narrative, each candidate resolved against real structural
data (fan_in/hotspot) where a module is named, composing on a required
`codebase-intelligence` report (ADR-010, eighth reuse). 47 tests, 8/8
evaluation fixtures on both layers. New ADR-018 documents the required-
composition reuse, the location resolver's word-boundary-correct-from-
day-one implementation (the fourth independent copy of the fix first
applied after L23/L24, and the first not shipped with the bug first), and
this skill's status as the first in the portfolio whose deterministic
layer targets a documentation artifact rather than a code-risk judgment.
A real dogfood run against genuine excerpts of this project's own
engineering history found a new, disclosed-not-fixed limitation (L28):
the resolver only checks the exact matched line, not the surrounding
paragraph, so every candidate in that real run resolved to no location at
all despite the relevant module being named four times nearby.

**Phase 13 onward**: the freeze from before Phase 11 remains in force,
now for a second consecutive phase boundary. The case for investing a
phase in the independent-evidence gap (L8/A5) before a thirteenth skill is
at least as strong as it was at the Phase 11 and Phase 12 boundaries — a
future session should weigh that explicitly before starting Phase 13, and
should not read Phase 11 or Phase 12 shipping as precedent that the freeze
auto-lifts on request alone without the user again making that call
explicitly, each time.

## Phase 13 — Context Optimizer (COMPLETE, 2026-08-26)

Per the roadmap's own phase list and full target skill portfolio
(`Advanced`: dependency-supply-chain-reviewer, engineering-knowledge-
capture, context-optimizer, workflow-composer, engineering-memory), Phase
13 was proposed as **Context Optimizer** — the third skill in the
`Advanced` group.

**How this actually started**: exactly as predicted in the "Phase 13
onward" note directly above — the freeze from before Phase 11 was still in
force, and the case for investing in L8/A5 instead of a thirteenth skill
was not weaker. The user then explicitly directed starting Phase 13
anyway, with their own stated exit criteria (same shape as Phase 11's and
Phase 12's: "same bar," first skill composing on `codebase-intelligence`'s
output — not literally true, the twelfth Pattern 2 reuse and ninth ADR-010
reuse, stated plainly in [[03-architecture]]/[[11-decisions]] — "scalable
and production-level stable"). This is a **third**, one-time,
user-authorized exception to the freeze, not evidence A2/A5 moved off
`UNKNOWN` — recorded here honestly, the same way Phase 11's and Phase 12's
exceptions were, rather than presented as if the freeze's conditions were
newly met.

**What shipped**: `context-optimizer` — a deterministic file-relevance and
context-budget engine: given a free-text task description and a required
`codebase-intelligence` report (ADR-010, ninth reuse), scores every file's
relevance via a tokenized whole-token keyword match, boosts the score with
real fan_in/hotspot structural data, and tiers each nonzero-scoring file
CORE/SUPPORTING/EXCLUDED, optionally against a line budget. 64 tests, 8/8
evaluation fixtures on both layers. New ADR-019 documents the
required-composition reuse, the relevance scorer's tokenized (not
`\b`-regex) technique — the fifth independent copy of the L23/L24-lineage
containment-check fix, the second built correct from day one — and this
phase's headline architectural decision: inverting the fail-closed-toward-
caution convention ADR-011/017/018 established into a fail-OPEN-toward-
inclusion default, since silently excluding a needed file is this skill's
worse failure mode, not silently including an unimportant one. A real
dogfood run against a real task description from this actual session found
a new, disclosed-not-fixed limitation (L29): at full-repository scale,
keyword relevance floods with false-positive CORE recommendations when the
task description shares this project's own recurring documentation/
evaluation-harness vocabulary — 5 of 17 CORE recommendations in the
dogfood run were unrelated files, not `context-optimizer` files, a new
manifestation of the same mechanism class `architecture-decision`'s
L14/L19/L21 already disclosed.

**Phase 14 onward**: the freeze from before Phase 11 remains in force, now
for a third consecutive phase boundary. The case for investing a phase in
the independent-evidence gap (L8/A5) before a fourteenth skill is at least
as strong as it was at the Phase 11, Phase 12, and Phase 13 boundaries — a
future session should weigh that explicitly before starting Phase 14, and
should not read Phase 11, Phase 12, or Phase 13 shipping as precedent that
the freeze auto-lifts on request alone without the user again making that
call explicitly, each time.

## Phase 14 — Workflow Composer (COMPLETE, 2026-08-26)

Per the roadmap's own phase list and full target skill portfolio
(`Advanced`: dependency-supply-chain-reviewer, engineering-knowledge-
capture, context-optimizer, workflow-composer, engineering-memory), Phase
14 was proposed as **Workflow Composer** — the fourth skill in the
`Advanced` group.

**How this actually started**: exactly as predicted in the "Phase 14
onward" note directly above — the freeze from before Phase 11 was still
in force, and the case for investing in L8/A5 instead of a fourteenth
skill was not weaker. The user then explicitly directed starting Phase 14
anyway, with their own stated exit criteria (same shape as Phase 11's,
12's, and 13's: "same bar," first skill composing on
`codebase-intelligence`'s output — not literally true, the thirteenth
Pattern 2 reuse and tenth ADR-010 reuse, stated plainly in
[[03-architecture]]/[[11-decisions]] — "scalable and production-level
stable"). Unlike Phase 11-13's reopenings, this one also directly
overrides a **named, phase-specific** decision already on record:
[[16-assumptions-and-validation]] A10 explicitly said "do not build
Workflow Composer (Phase 14) until Experiment B can be run." This is a
**fourth**, one-time, user-authorized exception to the freeze — and the
first one that overrides a decision naming the overridden phase by number
— not evidence A2/A5/A10 moved off `UNKNOWN`, recorded here honestly, the
same way Phase 11's, 12's, and 13's exceptions were, rather than presented
as if the freeze's or A10's conditions were newly met.

**What shipped**: `workflow-composer` — the first skill in the portfolio
whose deliverable is composed **execution**, not analysis. A deterministic
engine subprocess-sequences a small, hardcoded registry of exactly 3
workflow templates (`understand-then-plan`, `understand-then-test-plan`,
`understand-then-optimize-context`), each reusing a composition this
project already ran for real in an earlier phase's dogfood
(Phase 4's, Phase 3's real Pilot B, and Phase 13's, respectively), every
one rooted in a required `codebase-intelligence` report (ADR-010, tenth
reuse). 51 tests, 8/8 evaluation fixtures on both layers. New ADR-020
documents the required-composition reuse, this skill's status as the
first to invoke other skills' real code, and this phase's headline
architectural decision: failing **CLOSED** on execution uncertainty (a
compatibility-check drift blocks all real execution outright; any step's
failure stops the chain) — the opposite default from ADR-019's
content-inclusion inversion one phase earlier, explicitly framed as the
same underlying principle (fail toward the cheaper-to-recover-from error)
landing on the normal side because the cheaper error points the other way
in this domain. A real, non-dry-run execution against this repo's own
current state found a new, disclosed-not-fixed limitation (L30):
`feature-planner`'s own relevance scorer, composed via
`understand-then-plan`, ranked a test file above every real implementation
file relevant to the task — the same coincidental-keyword-collision
mechanism class `architecture-decision`'s L14/L19/L21 and
`context-optimizer`'s L29 already disclosed, now confirmed present inside
`feature-planner` itself, not just `context-optimizer`'s scorer.

**Phase 15 onward**: the freeze from before Phase 11 remains in force, now
for a fourth consecutive phase boundary. The case for investing a phase in
the independent-evidence gap (L8/A5) before a fifteenth skill is at least
as strong as it was at the Phase 11, Phase 12, Phase 13, and Phase 14
boundaries — a future session should weigh that explicitly before starting
Phase 15, and should not read Phase 11, Phase 12, Phase 13, or Phase 14
shipping as precedent that the freeze auto-lifts on request alone without
the user again making that call explicitly, each time. Phase 14
specifically should also not be read as evidence that a named,
phase-specific "do not build" decision (like A10's) can be routinely
overridden by request — this was recorded as a one-time exception, not a
new standing rule.
