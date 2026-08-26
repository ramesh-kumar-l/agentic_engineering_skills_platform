# Sprint 14 — Phase 14: Workflow Composer

## Goal
Build a fourteenth skill by reusing Pattern 2's judgment-based
architectural pattern a thirteenth time and the mandatory-composition rule
(ADR-010, already reused nine times) a tenth time, turning a registered
template name, a target repo, and a free-text task description into a
real, executed chain of this portfolio's own skill CLIs — the first
skill whose deliverable is composed execution, not analysis — per the
user's exit criteria ("same bar, first skill composing on top of
Codebase Intelligence's output, implementation make sure final developed
product is a scalable and production level stable system" — the "first"
framing is a tenth reuse of an already-established pattern, stated
honestly as such, same as every phase since Phase 6). The user also
directed strict per-file modularity (<300 lines) and a memory-bank
save-state update before ending — both already this project's standing
discipline, restated explicitly this sprint.

**Process context, unique to this sprint**: this is the FOURTH same-day
reopening of the mentor-review freeze, and the FIRST to also directly
override a named, phase-specific decision on record —
`16-assumptions-and-validation.md` A10 explicitly said "do not build
Workflow Composer (Phase 14) until Experiment B can be run." Phase 11,
Phase 12, and Phase 13 had already reopened the general freeze three
times earlier the same day; the freeze itself (A2/A5 both UNKNOWN, zero
real external users) had not lifted in between any of them, and A10's
specific "do not build" decision had not been revisited either. The user
then explicitly directed starting Phase 14 anyway. This sprint proceeded
on that explicit instruction — recorded here as a fourth, one-time
exception, not as the freeze's or A10's conditions having been met, and
not as Phase 11/12/13 shipping being read as precedent that asking
unfreezes the roadmap generally, or that a named "do not build" decision
can be routinely overridden.

## Hypothesis
Pattern 2 generalizes to a thirteenth judgment domain (deciding whether a
task actually fits a registered composition, and whether a real run's
chain of results is trustworthy) without needing a new base pattern.
Separately: a small, hardcoded registry of previously-dogfooded skill
compositions can be mechanized into real, subprocess-executed chains
without inventing new, unvalidated compositions — reusing exactly the
manual patterns Phase 3's Pilot B, Phase 4's dogfood, and Phase 13's
dogfood already proved out by hand.

## Success Criteria
Engine modules <300 lines each (met, max 152 lines — well under budget);
tests pass, including a CLI test file written from the start AND one
genuinely real subprocess-based integration test (a new discipline no
prior skill's suite exercised); evaluation harness runs against 8 seeded
fixtures with real scores for both layers; `SKILL.md` meets the canonical
template with explicit scope boundaries (no arbitrary skill chaining, no
target-repo mutation, not Experiment B) stated up front; memory bank
updated per the user's explicit "save state" directive; a real,
non-dry-run dogfood run against this project's own actual current state,
not a purely synthetic stand-in.

## Completed Work
`skills/workflow-composer/` (SKILL.md, engine — 12 modules, tests — 51
passing including CLI and one real subprocess-based integration test), an
8-fixture evaluation harness scoring deterministic step-status/
compatibility correctness plus judgment-layer Precision/Recall, a real
dogfood run (`examples/workflow-composer/`) executing `understand-then-plan`
for real against this repo's own current (fourteen-skill) state,
`project-memory-bank/05-evaluation-framework.md` (Workflow Composition
Checklist, thirteenth checklist), `11-decisions.md` (ADR-020),
`12-known-limitations.md` (L30, L8 update), `16-assumptions-and-
validation.md` (A2, A5, A10 updated), `03-architecture.md` (Pattern 2
reuse count updated), `08-roadmap.md` (Phase 14 marked complete with the
freeze/exception context), `implementation-status.md`,
`07-current-state.md`, `active-context.md`, root
`README.md`/`ROADMAP.md`/`CHANGELOG.md`, `.github/workflows/tests.yml`
(matrix updated), `.gitignore` (excludes the eval harness's generated
`_run/` directory).

## Evidence
51/51 new tests passing; 636/636 across all fourteen skills
(24+23+24+21+58+32+34+64+66+82+46+47+64+51). 8/8 evaluation fixtures:
deterministic layer 100% correct (automated — real registry templates run
against a bundled tiny fixture repo, fail-closed paths run against fixture
fake skills for determinism); judgment layer 8/8 perfect precision/recall
— same caveat as every prior phase, thirteenth time now, not read as
evidence of higher judgment quality than Phase 6's non-perfect case. Real
dogfood finding: a real, non-dry-run execution of `understand-then-plan`
against this repo's current (fourteen-skill) state, using a real task
description from this actual session, completed successfully (2 real
subprocess steps, 2.31s total, zero compatibility issues, 1,010 files
scanned) — but the composed `feature-planner` step's own relevance scorer
ranked a test file as the single highest-scoring file in the entire
repository, ahead of every real implementation file relevant to the task,
confirming the same keyword-flooding mechanism class `architecture-
decision`'s L21 and `context-optimizer`'s L29 already disclosed is present
inside `feature-planner` itself — logged as L30.

## Evaluation
Deterministic dimensions (step statuses, compatibility-issue count,
dry-run side-effect absence, CLI exit code) fully automated, same
discipline as Phases 1-13, extended here to include a genuinely real
subprocess execution path (not just synthetic report scoring) as part of
the deterministic layer for the first time. Judgment-layer Precision/
Recall computed automatically from real agent-produced `actual/*.json`,
same methodology as every prior phase. Safety/Explainability left for
human review, same discipline as before. All 8 fixtures' expected results
were authored before any actual derivation was scored against them, same
protocol as every prior phase. Case-05 exercises fail-closed
chain-stopping on a real (fixture) subprocess failure; case-06 exercises
the compatibility-drift pre-execution gate, a distinct fail-closed
mechanism from case-05's step-failure handling.

## Failures
None shipped as an undisclosed defect. One gap was found via real
dogfood, after fixtures already passed, and disclosed rather than
silently patched around: composing with `feature-planner` inherits that
skill's own keyword-flooding susceptibility unfiltered (L30, above). Left
unfixed by design — the same "disclose, don't guess a fix from one data
point" discipline this project applied to L14, L18, L21, L22, and L29 on
their first discovery, and the same mechanism class `architecture-
decision`'s L21 and `context-optimizer`'s L29 already named without a fix
being built. Separately, an early design draft of `step_runner.py` wrote
task text to a file using the same code path for both `codebase-
intelligence`'s repo-path positional argument and every downstream step's
task-text positional argument — caught during implementation, before any
test was written against it, and fixed by splitting `run_step`'s
API so the caller (`executor.py`) supplies an already-resolved
`positional_arg` (the repo path for step 1, a prepared task file for every
downstream step) rather than `step_runner.py` guessing which shape a given
step needs.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (the
deterministic layer's synthetic-fixture cases complete in low
milliseconds; the two real registry-template dry-run and real-execution
paths complete in low seconds, consistent with the dogfood run's own
2.31s total) and test/fixture pass rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-020 (required composition reused a tenth time; first skill whose
engine invokes other skills' real code via subprocess; fails CLOSED on
execution uncertainty — the opposite default from ADR-019, framed
explicitly as the same underlying principle landing on the normal side
because the cheaper error points the other way in this domain; registry
deliberately bounded to 3 hardcoded, previously-dogfooded templates rather
than a generic arbitrary-skill chainer) — see `11-decisions.md`. Pattern 2
(ADR-007) reused a thirteenth time without a new base-pattern ADR.

## Lessons Learned
A fail-closed default and a fail-open default can coexist in the same
project without contradiction, as long as each is traced back to the same
underlying principle (fail toward the cheaper-to-recover-from error) and
the reasoning for which direction is cheaper in THIS domain is stated
explicitly — ADR-020's fail-closed execution default and ADR-019's
fail-open content-inclusion default, one phase apart, are the clearest
demonstration yet that this project's conventions are principle-driven,
not just pattern-copied forward by default. Separately: composing with an
existing skill does not inherit that skill's limitations by magic — it
inherits them literally and silently unless the composing skill's own
report explicitly says so, which `WorkflowRunReport` does not yet do; this
is itself worth naming as a gap for a future session to consider, not
something to quietly patch into this sprint's already-approved scope.

## What We Should Stop / Continue / Change
- **Continue**: reusing already-proven manual compositions (Pilot B,
  Phase 4's dogfood, Phase 13's dogfood) as the seed for a new template,
  rather than inventing untested compositions and hoping they work — this
  sprint's 3-template registry is bounded specifically because of this
  discipline.
- **Continue**: real dogfood runs against genuine project material (this
  session's own task, not synthetic text) even when — especially when —
  the result surfaces a limitation in a skill built four phases earlier
  (`feature-planner`, Phase 4) rather than in this sprint's own new code.
- **Change (carried over from Sprints 05-13, now fourteen skills deep)**:
  the independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was started at explicit user direction that reopened, for a fourth
  time, rather than resolved, the same-day freeze on new-skill work, and
  for the first time also overrode a decision (A10) that named this exact
  phase by number. The case for investing a sprint in L8/A5 before a
  fifteenth skill remains at least as strong as it was going into this
  sprint, arguably stronger now that it has been deferred four times in
  one day, the last one overriding a specific "do not build" decision.

## Next Sprint Recommendation
No Phase 15 by default. The freeze from before Sprint 11 remains in
force, now deferred across four consecutive phase boundaries: re-justify
against real external validation evidence (a real user, an
independent/blind eval pass, or a real usage-comparison run) before
starting any further skill phase, per the adaptive-roadmap rule — this
sprint's own existence is not that evidence, and should not be read as
precedent that asking unfreezes the roadmap generally, or that a named
"do not build" decision (like A10's) can be routinely overridden by
request.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill that actually executes other real skills — not a prototype or a paper plan |
| Technical Quality | 4 | Modular (<300 lines/file, max 152), tested including one genuinely real subprocess integration test, pattern reuse worked cleanly, the fail-closed default is a real, justified design decision explicitly reconciled with ADR-019's opposite default |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one real dogfood run mostly surfaced a limitation inherited from a composed skill (L30) rather than delivering a clean, trustworthy end-to-end result on its own |
| Evaluation Quality | 3 | Deterministic layer solid and, for the first time, partly grounded in real subprocess execution rather than only synthetic fixtures; judgment layer is self-authored/single-rater for the thirteenth time |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, ADR-020, known limitations, and the dogfood example all recorded with concrete evidence, including the honest real-timing disclosure and the explicit "this is not Experiment B" reminder throughout |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep beyond the approved plan |
| Learning | 4 | The cross-skill keyword-flooding finding (L30) is a genuinely new, concrete instance of an already-named mechanism class in a DIFFERENT skill's code than where it was first found — and the fail-closed/fail-open reconciliation with ADR-019 is a new architectural discipline in its own right |
