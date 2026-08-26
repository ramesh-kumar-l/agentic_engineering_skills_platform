# Sprint 11 — Phase 11: Dependency / Supply Chain

## Goal
Build an eleventh skill by reusing Pattern 2's judgment-based architectural
pattern a tenth time and the mandatory-composition rule (ADR-010, already
reused six times) a seventh time, turning a required `codebase-
intelligence` report into a Dependency Risk Report — pin status, known-risk
name matches, duplicate/conflicting version declarations, and surface
area — per the user's exit criteria ("same bar, first skill composing on
top of Codebase Intelligence's output, make sure final developed product is
a scalable and production level stable system" — the "first" framing is a
seventh reuse of an already-established pattern, stated honestly as such,
same as every phase since Phase 6).

**Process context, unique to this sprint**: earlier the same day, a
mentor-style critique of the whole project (requested by the user)
concluded velocity of building had outpaced velocity of validating (A2/A5
both UNKNOWN after ten phases, zero real external users) and froze the
roadmap pending real validation evidence. The user then explicitly directed
starting Phase 11 anyway. This sprint proceeded on that explicit
instruction — recorded here as a one-time exception, not as the freeze's
conditions having been met.

## Hypothesis
Pattern 2 generalizes to a tenth judgment domain (assessing supply-chain
hygiene risk) without needing a new base pattern. Separately: real,
offline-checkable dependency risk exists between "ignore `requirements.txt`
entirely" and "run a live CVE scanner this project deliberately doesn't
have" — pin status, exact-name known-risk matches, and cross-manifest
version conflicts are all derivable from data `codebase-intelligence`
already parses, without fabricating signal (like per-dependency license
risk) that isn't actually available.

## Success Criteria
Engine modules <300 lines each (met, max 88 lines — well under budget);
tests pass, including a CLI test file written from the start; evaluation
harness runs against 8 seeded fixtures with real scores for both layers;
`SKILL.md` meets the canonical template with explicit scope boundaries (no
CVE lookup, no license-risk detection) stated up front, not discovered
later; memory bank updated per the user's "save state" requirement; a real
dogfood run against this repo's own actual manifests, not a purely
synthetic stand-in.

## Completed Work
`skills/dependency-supply-chain/` (SKILL.md, engine — 11 modules, tests —
46 passing including CLI), an 8-fixture evaluation harness scoring
deterministic flag-set/risk-level correctness plus judgment-layer
Precision/Recall, a dogfood run (`examples/dependency-supply-chain/`)
against this repo's own real root manifest, `project-memory-bank/
05-evaluation-framework.md` (Dependency Risk Checklist added, tenth
checklist), `11-decisions.md` (ADR-017), `12-known-limitations.md` (L25,
L26), `16-assumptions-and-validation.md` (A2, A5 notes), `08-roadmap.md`
(Phase 11 marked complete with the freeze/exception context), `
implementation-status.md`, `07-current-state.md`, `active-context.md`, root
`README.md`/`ROADMAP.md`/`CHANGELOG.md`, `.github/workflows/tests.yml`
(matrix updated).

## Evidence
46/46 new tests passing; 474/474 across all eleven skills
(24+23+24+21+58+32+34+64+66+82+46). 8/8 evaluation fixtures: deterministic
layer 100% correct (automated); judgment layer 8/8 perfect precision/
recall — same caveat as every prior phase, tenth time now, not read as
evidence of higher judgment quality than Phase 6's non-perfect case. Real
dogfood finding: run against this repo's own root, only 1 real dependency
(`pytest`) was visible — a concrete, live confirmation of the inherited L2
root-level-only scope limitation (this platform's actual per-skill
dependencies live in `skills/*/pyproject.toml`, one level below repo root,
which `codebase-intelligence`'s parser doesn't recursively scan).

## Evaluation
Deterministic dimensions (Correctness/Efficiency) fully automated, same as
Phases 1-10. Judgment-layer Precision/Recall computed automatically from
real agent-produced `actual/*.json`, same methodology as every prior phase.
Safety/Explainability left for human review, same discipline as before. All
8 fixtures' expected categories were authored before any actual derivation
was scored against them, same protocol as every prior phase. Case-07
deliberately exercises multi-flag composition (a wildcard, a known-risk
name, and a duplicate-conflict all firing at once), and case-08 exercises
the fail-closed rule (zero dependencies found triggers `REQUIRES_REVIEW`,
never a silent `CLEAR`).

## Failures
None shipped as an undisclosed defect. One planned feature was caught and
dropped before shipping, not after: the original scope included
per-dependency license-risk detection (`license_patterns.py`); during
implementation it became clear this data doesn't actually exist in what
`codebase-intelligence` parses (a manifest's `license` field describes the
project's own license, not each dependency's) — building it anyway would
have shipped a fabricated-looking flag. It was dropped and named explicitly
as L26 instead, the same self-correction discipline this project applied to
the L24 test-design catch in the mentor-review pass earlier the same day.

## Metrics
Not tracked as "number of prompts" — see evaluation harness timing (all
fixtures well under 1ms for the deterministic layer) and test/fixture pass
rates above.

## Community Feedback
None — not yet published externally.

## Decisions
ADR-017 (required composition reused a seventh time; two explicit scope
decisions — no live CVE/vulnerability-database lookup, no per-dependency
license-risk detection — stated as disclosed boundaries, not silent gaps;
ADR-011's advisory/fail-closed discipline reused a second time) — see
`11-decisions.md`. Pattern 2 (ADR-007) reused a tenth time without a new
base-pattern ADR.

## Lessons Learned
Reusing CI's already-parsed `external_dependencies` field instead of
re-parsing manifests avoided an eleventh copy of manifest-parsing logic,
but also meant inheriting a scope gap (L2) invisibly until the real dogfood
run made it concrete — a reminder that composing on another skill's output
means composing on its blind spots too, not just its data. Separately, the
license-risk scope correction is this sprint's most important finding: the
original plan assumed license data was available from the same manifests
already being read, and that assumption was wrong — caught by actually
tracing where the data would come from before writing the detector, not
after shipping a plausible-looking but ungrounded flag.

## What We Should Stop / Continue / Change
- **Continue**: catching scope assumptions that don't hold before shipping,
  not after — the license-risk drop this sprint is the same discipline as
  the L24 test-design catch earlier the same day, applied at design time
  instead of at test-writing time.
- **Continue**: real dogfood runs against this repo's own state, even when
  the result is "found almost nothing" — the near-empty result here was
  itself the most informative finding (concretely demonstrating L2's
  scope), not a wasted run.
- **Change (carried over from Sprints 05-10, now ten skills deep)**: the
  independent-rater evaluation (L8) and the inter-rater-agreement
  experiment (A5) remain unrun. This sprint did not close that gap — it was
  started at explicit user direction that reopened, rather than resolved,
  the same-day freeze on new-skill work. The case for investing a sprint in
  L8/A5 before a twelfth skill remains at least as strong as it was going
  into this sprint.

## Next Sprint Recommendation
No Phase 12 by default. The freeze from before this sprint remains in
force: re-justify against real external validation evidence (a real user,
an independent/blind eval pass, or a real usage-comparison run) before
starting any further skill phase, per the adaptive-roadmap rule — this
sprint's own existence is not that evidence, and should not be read as
precedent that asking unfreezes the roadmap generally.

## Sprint Score (honest, not inflated)

| Dimension | Score /5 | Note |
|---|---|---|
| Shipped Value | 4 | Real, working, tested skill — not a prototype |
| Technical Quality | 4 | Modular (<300 lines/file, max 88), tested, pattern reuse worked cleanly, the license-risk scope correction is a real design decision, not cosmetic |
| Usefulness | 2 | Not yet used on real engineering work by anyone else; the one dogfood run is a real but self-run, near-empty result |
| Evaluation Quality | 3 | Deterministic layer solid; judgment layer is self-authored/single-rater for the tenth time; perfect fixture scores are less informative than the real dogfood finding this sprint |
| Real-world Validation | 0 | Zero external usage |
| Community Value | 0 | Not published |
| Documentation | 5 | SKILL.md, ADR-017, known limitations, and the dogfood example all recorded with concrete evidence, including the honest license-risk scope-drop disclosure |
| Focus | 4 | One skill plus the explicitly-requested modularity/save-state discipline; no scope creep beyond the one corrected drop |
| Learning | 3 | The license-risk scope correction is a genuinely new finding; the rest largely confirms patterns already established across ten prior phases |
