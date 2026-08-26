# Sprint 15 — Phase 15: Engineering Memory

## Goal
Build a fifteenth skill by reusing Pattern 2's judgment-based
architectural pattern a fourteenth time and the mandatory-composition rule
(ADR-010, already reused ten times) an eleventh time, turning a free-text
task description into a ranked retrieval of this project's own recorded
ADRs and known limitations — the first skill whose primary input corpus
is this project's own memory bank rather than a target repo's external
artifacts — per the user's exit criteria ("same bar, first skill
composing on top of Codebase Intelligence's output, implementation make
sure final developed product is a scalable and production level stable
system" — the "first" framing is an eleventh reuse of an already-
established pattern, stated honestly as such, same as every phase since
Phase 6). The user also directed strict per-file modularity (<300 lines)
and a memory-bank save-state update before ending — both already this
project's standing discipline, restated explicitly this sprint.

**Process context, unique to this sprint**: this is the FIFTH same-day
reopening of the mentor-review freeze, but a different shape than Phase
14's. Phase 14 jumped ahead of a named, phase-specific "do not build"
decision (A10). Phase 15 did not — `16-assumptions-and-validation.md` A8
gated Engineering Memory with "do not implement early; design only when
reached," and Phase 15 is being reached in its designated order, the
fifth and final skill in the `Advanced` portfolio group. The *general*
freeze (A2/A5 both UNKNOWN, zero real external users) is still not
satisfied — the user's explicit direction overrides it, same as Phase
11-14, not new evidence that it lifted.

## Hypothesis
Pattern 2 generalizes to a fourteenth judgment domain (deciding whether a
retrieved memory-bank record is actually relevant to a task, and how much
weight a staleness flag should carry) without needing a new base pattern.
Separately: applying the word-boundary/whole-token matching technique
this project has now proven correct in two prior skills (`context-
optimizer`'s ADR-019, `engineering-knowledge-capture`'s ADR-018) from the
very first line of a new skill's code — rather than shipping the naive
substring version and discovering the bug via a real dogfood run, the way
`target_resolver.py`'s first three copies did — actually works, and any
real residual gap found via dogfood is a genuinely new failure mode, not
a repeat of the already-known one.

## Success Criteria
Engine modules <300 lines each (met, max 148 lines — well under budget);
tests pass, including a CLI test file written from the start AND one
genuinely real end-to-end integration test (parsing real-shaped memory-
bank fixtures through the full pipeline); evaluation harness runs against
8 seeded fixtures with real scores for both layers, including a
proactive regression test for the exact substring-collision class this
project has now disclosed eight times; `SKILL.md` meets the canonical
template with explicit scope boundaries (no memory-bank writes, no
duplicate-detection bridge to `engineering-knowledge-capture`, corpus
limited to 2 files this pass) stated up front; memory bank updated per
the user's explicit "save state" directive; a real, non-fixture dogfood
run against this project's own actual memory bank, not a purely synthetic
stand-in.

## Completed Work
`skills/engineering-memory/` (SKILL.md, engine — 12 modules, tests — 57
passing including CLI and one real end-to-end integration test), an
8-fixture evaluation harness scoring deterministic match/staleness/
count/error/warning correctness plus judgment-layer Precision/Recall, a
real dogfood run (`examples/engineering-memory/`) retrieving against
this project's own actual 50-record memory bank (20 decisions, 30
limitations) using a freshly-generated real `codebase-intelligence`
report, `project-memory-bank/05-evaluation-framework.md` (Engineering
Memory Retrieval Checklist, fourteenth checklist), `11-decisions.md`
(ADR-021), `12-known-limitations.md` (L31, L8 update), `16-assumptions-
and-validation.md` (A2, A5, A8 updated), `03-architecture.md` (Pattern 2
reuse count updated), `08-roadmap.md` (Phase 15 marked complete, no
Phase 16 exists), `implementation-status.md`, `07-current-state.md`,
`active-context.md`, root `README.md`/`ROADMAP.md`/`CHANGELOG.md`,
`.github/workflows/tests.yml` (matrix updated).

## Evidence
57/57 new tests passing; 693/693 across all fifteen skills
(24+23+24+21+58+32+34+64+66+82+46+47+64+51+57). 8/8 evaluation fixtures:
deterministic layer 100% correct (automated — real memory-bank-shaped
fixtures, including a genuine whole-token-vs-substring case where a
coincidental low-score match correctly ranks below the real one rather
than being excluded outright); judgment layer 8/8 perfect precision/
recall — same caveat as every prior phase, fourteenth time now, not read
as evidence of higher judgment quality than Phase 6's non-perfect case.
Real dogfood finding: a real retrieval run against this project's own
current 50-record memory bank, using a real task description from this
actual session, retrieved 8 substantively on-topic matches and correctly
flagged both real staleness signals encountered (a real `FIXED` title on
L23, a real missing-module mention on ADR-017) — but found a new,
disclosed-not-fixed limitation: `module_resolver.py`'s basename-exact
resolution, built correct from day one specifically to defeat the
substring-collision class, still collapses every mention of a basename
shared across many real skills (`ci_report_loader.py`) into the same
single, arbitrarily-chosen resolved path — five different real records
about five different skills (ADR-016, L24, ADR-020, ADR-015, ADR-017) all
resolved to the same `root-cause-analyzer` copy — logged as L31.

## Evaluation
Deterministic dimensions (which record ids match, which are flagged
stale, match count / raised-error / warning behavior) fully automated,
same discipline as Phases 1-14. Judgment-layer Precision/Recall computed
automatically from real agent-produced `actual/*.json`, same methodology
as every prior phase. Safety/Explainability left for human review, same
discipline as before. All 8 fixtures' expected results were authored
before any actual derivation was scored against them, same protocol as
every prior phase, with one honest mid-build correction: case-03's
`expected_absent_ids` design was replaced with `expected_rank_order`
after the real engine run showed a genuine (not a bug) low-score
coincidental match via an unrelated skill-name mention — the fixture was
adjusted to test the actually-correct property (the real match outranks
the coincidental one) rather than forcing an unrealistic zero-overlap
scenario.

## Failures
None shipped as an undisclosed defect. One design correction was made
mid-build, before any test was written against the wrong behavior: the
first draft of case-03's evaluation fixture assumed a genuinely
unrelated record would score exactly zero against the task keywords;
running it for real showed a low, honest nonzero score via a legitimate
whole-token hit on a skill-name mention (`acceptance-test-engineer`
tokenizing into `acceptance`/`test`/`engineer`), which is not a bug — the
fixture's expectation was corrected to check relative rank instead of
absence, which is the property that actually matters and the one this
project's own real limitations (L21/L29/L30) describe. Separately, one
gap was found via real dogfood, after fixtures already passed, and
disclosed rather than silently patched around: the basename-exact module
resolver collapses distinct same-basename files across the portfolio
into one match (L31, above). Left unfixed by design — the same "disclose,
don't guess a fix from one data point" discipline this project applied to
L14, L18, L21, L22, L23, L24, L28, L29, and L30 on their first discovery.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
cases complete in under 1ms against the fixture repo) and test/fixture
pass rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-021 (required composition reused an eleventh time; first
self-referential-composition skill, retrieving against this project's own
memory bank rather than a target repo's artifacts; word-boundary/
whole-token matching applied from day one, an accumulated lesson applied
rather than a new one discovered; stays on the normal fail-closed-toward-
caution side for staleness, not ADR-019's inversion) — see
`11-decisions.md`. Pattern 2 (ADR-007) reused a fourteenth time without a
new base-pattern ADR.

## Lessons Learned
Building a technique "correct from day one" to defeat one specific,
already-disclosed failure mode (substring collision) does not imply every
related failure mode in the same code is also solved — L31 is a
genuinely different ambiguity (multiple TRUE matches sharing a basename,
not a FALSE match from containment) that the same exact-basename design
choice does not and cannot address, discovered only once real data (this
project's own many-skill memory bank, where file-naming conventions are
deliberately consistent) was run through the pipeline. Separately: an
evaluation fixture's expectation should be corrected to match what a real
engine run actually and legitimately produces, not forced to match a
prior assumption about what "should" happen — case-03's mid-build
correction is a concrete instance of that discipline, done before any
test was written against the wrong expectation, not after a failure was
rationalized away.

## What We Should Stop / Continue / Change
- **Continue**: applying an already-proven technique (word-boundary/
  whole-token matching) from day one in a new skill rather than shipping
  the naive version and waiting for a dogfood run to find the bug — this
  sprint's real dogfood run still found something (L31), but a materially
  different and narrower gap than the class this discipline was built to
  prevent.
- **Continue**: real dogfood runs against genuine project material (this
  project's own actual memory bank, not synthetic text) even at the very
  end of a long sequence of phases, when it would be tempting to assume
  "we've done this enough times, it'll be clean."
- **Change (carried over from Sprints 05-14, now fifteen skills deep)**:
  the independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it
  was started at explicit user direction that reopened, for a fifth time,
  the same-day freeze on new-skill work. Unlike Phase 14, this reopening
  did not need to override a named "do not build" decision, since Phase
  15 was reached in its designated order — but the underlying gap (zero
  real external users, A2/A5 both UNKNOWN) is unchanged by that
  distinction. With the originally-scoped 15-skill portfolio now complete,
  the case for investing a phase in L8/A5 before proposing any further
  skill is stronger than at any prior boundary — there is no longer a
  pre-written "next skill" to default to.

## Next Sprint Recommendation
No further skill by default — the originally-scoped 15-skill portfolio
named in `08-roadmap.md` is now complete, and no Phase 16 exists in that
list. The freeze from before Sprint 11 remains in force, now deferred
across five consecutive phase boundaries: re-justify against real
external validation evidence (a real user, an independent/blind eval
pass, or a real usage-comparison run) before proposing any further skill
phase, per the adaptive-roadmap rule — this sprint's own existence is not
that evidence, and should not be read as precedent that asking unfreezes
the roadmap generally.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill that retrieves against this project's own real memory bank and correctly flags real staleness — not a prototype or a paper plan |
| Technical Quality | 4 | Modular (<300 lines/file, max 148), tested including a real end-to-end integration test, pattern reuse worked cleanly, the day-one word-boundary discipline is a real, verifiable design choice, not just a claim |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one real dogfood run mostly demonstrated correct retrieval while also surfacing a new, disclosed limitation (L31) rather than delivering a fully clean result |
| Evaluation Quality | 3 | Deterministic layer solid and grounded in real memory-bank-shaped fixtures, including a proactive regression test for a well-established failure class; judgment layer is self-authored/single-rater for the fourteenth time |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, ADR-021, known limitations, and the dogfood example all recorded with concrete evidence, including the honest real-numbers disclosure and the explicit "this is not evidence for A8" reminder throughout |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep beyond the approved plan |
| Learning | 4 | The L31 finding is a genuinely new, concrete instance of a DIFFERENT failure mode than the one this skill's own resolver was built correct-from-day-one to prevent — a sharper lesson than "the same bug recurred," namely "solving one failure mode doesn't imply an adjacent one is also solved" |
