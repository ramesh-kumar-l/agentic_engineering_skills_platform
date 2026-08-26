# Sprint 13 — Phase 13: Context Optimizer

## Goal
Build a thirteenth skill by reusing Pattern 2's judgment-based
architectural pattern a twelfth time and the mandatory-composition rule
(ADR-010, already reused eight times) a ninth time, turning a free-text
task description and a required `codebase-intelligence` report into a
Context Optimization Report — a ranked, budget-aware CORE/SUPPORTING/
EXCLUDED file recommendation list, grounded in real keyword relevance and
structural (fan_in/hotspot) data — per the user's exit criteria ("same
bar, first skill composing on top of Codebase Intelligence's output,
implementation make sure final developed product is a scalable and
production level stable system" — the "first" framing is a ninth reuse of
an already-established pattern, stated honestly as such, same as every
phase since Phase 6). The user also directed strict per-file modularity
(<300 lines) and a memory-bank save-state update before ending — both
already this project's standing discipline, restated explicitly this
sprint.

**Process context, unique to this sprint**: this is the THIRD same-day
reopening of the mentor-review freeze. Phase 11 (`dependency-supply-chain`)
and Phase 12 (`engineering-knowledge-capture`) had already reopened it
twice earlier the same day at the user's explicit direction; the freeze
itself (A2/A5 both UNKNOWN, zero real external users) had not lifted in
between either time. The user then explicitly directed starting Phase 13
anyway. This sprint proceeded on that explicit instruction — recorded here
as a third, one-time exception, not as the freeze's conditions having been
met, and not as Phase 11 or Phase 12 shipping being read as precedent that
asking unfreezes the roadmap generally.

## Hypothesis
Pattern 2 generalizes to a twelfth judgment domain (deciding what context
an agent actually needs for a task) without needing a new base pattern.
Separately: a task-relevance signal built from real, tokenized keyword
matching against structural metadata already in a `codebase-intelligence`
report — boosted by real fan_in/hotspot data, tiered against an optional
line budget — can produce a usable file recommendation without fabricating
judgment about which files are actually sufficient for the task.

## Success Criteria
Engine modules <300 lines each (met, max 95 lines — well under budget);
tests pass, including a CLI test file written from the start; evaluation
harness runs against 8 seeded fixtures with real scores for both layers;
`SKILL.md` meets the canonical template with explicit scope boundaries
(no semantic/embedding search, no automatic context loading) stated up
front; memory bank updated per the user's explicit "save state" directive;
a real dogfood run against this project's own actual engineering session,
not a purely synthetic stand-in.

## Completed Work
`skills/context-optimizer/` (SKILL.md, engine — 13 modules, tests — 64
passing including CLI), an 8-fixture evaluation harness scoring
deterministic recommendation-set/tier/oversized-flag correctness plus
judgment-layer Precision/Recall, a dogfood run
(`examples/context-optimizer/`) against a real task description from this
actual session, `project-memory-bank/05-evaluation-framework.md` (Context
Optimization Checklist added, twelfth checklist), `11-decisions.md`
(ADR-019 — also fixed a pre-existing structural bug found while editing
this file: ADR-017's own decision-checklist bullets had been misplaced
after ADR-018's, corrected back to ADR-017's section), `12-known-
limitations.md` (L29), `16-assumptions-and-validation.md` (A2, A5 notes),
`03-architecture.md` (Pattern 2 reuse count updated), `08-roadmap.md`
(Phase 13 marked complete with the freeze/exception context),
`implementation-status.md`, `07-current-state.md`, `active-context.md`,
root `README.md`/`ROADMAP.md`/`CHANGELOG.md`, `.github/workflows/tests.yml`
(matrix updated).

## Evidence
64/64 new tests passing; 585/585 across all thirteen skills
(24+23+24+21+58+32+34+64+66+82+46+47+64). 8/8 evaluation fixtures:
deterministic layer 100% correct (automated); judgment layer 8/8 perfect
precision/recall — same caveat as every prior phase, twelfth time now, not
read as evidence of higher judgment quality than Phase 6's non-perfect
case. Real dogfood finding: a fresh codebase-intelligence report against
this repo's current (thirteen-skill) state, scored against a real task
description drawn from this actual session, produced 17 CORE
recommendations — 12 genuinely `context-optimizer` files, but 5 were
unrelated files (four other skills' `run_evaluation.py` boilerplate plus
one unrelated fixture) scoring as high as or higher than several
genuinely relevant engine files, purely because this project's own
evaluation-harness docstrings repeat the same vocabulary across every
skill — logged as L29.

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-12. Judgment-layer Precision/Recall computed automatically from
real agent-produced `actual/*.json`, same methodology as every prior
phase. Safety/Explainability left for human review, same discipline as
before. All 8 fixtures' expected recommendation sets were authored before
any actual derivation was scored against them, same protocol as every
prior phase. Case-04 deliberately exercises budget-constrained EXCLUDED
tiering (two equal-scoring SUPPORTING candidates both correctly excluded
once the one CORE candidate consumes part of the budget), and case-05
exercises the fail-OPEN rule (a single oversized file is flagged, never
silently dropped, even though it alone exceeds the budget).

## Failures
None shipped as an undisclosed defect. One gap was found via real
dogfood, after fixtures already passed, and disclosed rather than
silently patched around: `relevance_scorer.py`'s inability to distinguish
genuine task relevance from corpus-wide vocabulary reuse at full-
repository scale (L29, above). Left unfixed by design — the same
"disclose, don't guess a fix from one data point" discipline this project
applied to L14, L18, L21, and L22 on their first discovery, and the same
mechanism class `architecture-decision`'s L21 already named without a fix
being built.

Separately, while editing `project-memory-bank/11-decisions.md` to append
ADR-019, found and fixed a pre-existing structural bug unrelated to this
sprint's own work: ADR-017's decision-checklist bullets (User Value/
Correctness/Security/etc.) had been misplaced after ADR-018's own
"Status: Adopted" line instead of appearing in ADR-017's own section,
leaving ADR-017 without a checklist and ADR-018 with two. Corrected by
moving the block back to ADR-017's section — confirmed via the block's own
content (`pin_checker.py`/`risk_patterns.py`/"L8, now tenth time" — all
Phase 11/`dependency-supply-chain` details) that it unambiguously belonged
there, not left as a judgment call.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures well under 1ms for the deterministic layer) and test/fixture pass
rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-019 (required composition reused a ninth time; relevance scorer built
as the fifth independent copy of the L23/L24-lineage containment check,
using tokenization rather than a `\b` regex, a disclosed different
precision/recall tradeoff than Phase 12's `location_resolver.py`; the
fail-closed-toward-caution convention ADR-011/017/018 established is
deliberately inverted into a fail-OPEN-toward-inclusion default, since
under-recommending context is this skill's worse failure mode) — see
`11-decisions.md`. Pattern 2 (ADR-007) reused a twelfth time without a new
base-pattern ADR.

## Lessons Learned
Inverting an established convention (fail-closed -> fail-open) is only
defensible when the reason the convention existed in the first place is
made explicit and shown not to apply the same way here — "fail toward the
cheaper-to-recover-from error" is the actual underlying principle behind
ADR-011/017/018's fail-closed default, and stating that principle
explicitly (rather than just "we do it differently this time") is what
keeps the inversion from reading as an inconsistency. Separately: choosing
a genuinely different technique (tokenization) instead of copying
`location_resolver.py`'s `\b`-regex verbatim, once it became clear the
regex approach would silently fail on this skill's own snake_case-heavy
target text, is a case where "reuse the same fix" would have been the
wrong move — worth naming explicitly rather than reusing precedent by
default.

## What We Should Stop / Continue / Change
- **Continue**: naming a disclosed tradeoff precisely instead of reaching
  for the nearest prior fix by default — this sprint's tokenized scorer is
  a genuinely different technique from Phase 12's regex, chosen because
  the target text's shape (snake_case file paths) made the regex approach
  systematically wrong here, not just "different for variety."
- **Continue**: real dogfood runs against genuine project material (this
  session's own task, not synthetic text) even when — especially when —
  the result contradicts every evaluation fixture's assumption (the small,
  isolated fixtures could not have caught L29's full-repository-scale
  effect).
- **Change (carried over from Sprints 05-12, now thirteen skills deep)**:
  the independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was started at explicit user direction that reopened, for a third time,
  rather than resolved, the same-day freeze on new-skill work. The case
  for investing a sprint in L8/A5 before a fourteenth skill remains at
  least as strong as it was going into this sprint, arguably stronger now
  that it has been deferred three times in one day.

## Next Sprint Recommendation
No Phase 14 by default. The freeze from before Sprint 11 remains in force,
now deferred across three consecutive phase boundaries: re-justify against
real external validation evidence (a real user, an independent/blind eval
pass, or a real usage-comparison run) before starting any further skill
phase, per the adaptive-roadmap rule — this sprint's own existence is not
that evidence, and should not be read as precedent that asking unfreezes
the roadmap generally.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file, max 95), tested, pattern reuse worked cleanly, the fail-OPEN inversion is a real, justified design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is a real but self-run result that mostly surfaced a limitation (keyword flooding at scale) rather than delivering a clean, trustworthy recommendation set |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the twelfth time; perfect fixture scores are less informative than the real dogfood finding this sprint |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, ADR-019, known limitations, and the dogfood example all recorded with concrete evidence, including the honest full-repository-scale flooding disclosure and the exact CORE-tier noise count |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep (the incidental ADR-017/018 structural fix was a one-line-scope correction, not new work) |
| Learning | 4 | The full-repository-scale keyword-flooding finding is a genuinely new, concrete instance of an already-named mechanism class (L14/L19/L21), not just a repeat confirmation — and the fail-OPEN inversion is a new architectural pattern in its own right |
