# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 7 (architecture-decision) — COMPLETE. Phase 8 (Refactoring Safety, per
[[08-roadmap]]'s reordering note — originally proposed as Phase 7) not
started, still waiting on explicit user instruction per [[08-roadmap]]'s
phase protocol.

## What Phase 7 built

Built `architecture-decision`, the seventh skill: `SKILL.md` contract
reusing Pattern 2 (ADR-007) a sixth time — a deterministic engine (11
modules, each under 300 lines) that parses a decision description into
distinct options (explicit `Option A:` markers, numbered/lettered lists, or
a `vs`/`versus` fallback split), then scores each option's structural blast
radius against `codebase-intelligence`'s real dependency graph, rolling
keyword relevance up into a `low`/`medium`/`high` tier driven by real
fan-in and hotspot data. 34 passing tests, including a CLI test file
written from the start (same discipline Phases 5-6 established). Combined
with an agent-driven Architecture Decision Record checklist workflow — a
new, sixth checklist in [[05-evaluation-framework]] (10 categories: context,
alternatives identified, decision stated, consequences per option,
reversibility, blast radius grounded in real data, security implications,
evidence cited, revisit trigger, assumption flag).

**Architecture**: reuses `feature-planner`'s/`root-cause-analyzer`'s
mandatory-composition rule (ADR-010) a third time — a missing/malformed
`codebase-intelligence` report is a hard failure, not a degraded path,
stated explicitly as a *reuse*. New this phase: **ADR-013** — each option's
blast radius is scored in a three-tier structural-risk band
(`hotspot_count > 0` or `blast_radius_score >= 10` forces `high`) rather
than a bare relevance number, so an option touching a real hotspot is never
presented with the same confidence as one touching nothing real.

**Phase ordering note**: the roadmap previously proposed Phase 7 as
Refactoring Safety (Architecture Decision at Phase 8). The user's Phase 7
instruction explicitly named "Architecture Decision" — a real reordering,
stated plainly in [[08-roadmap]] rather than silently drifted past.
Refactoring Safety now sits at Phase 8.

**Evaluation**: an 8-fixture harness (`evaluations/architecture-decision/`),
same two-layer scoring (deterministic + judgment) as Phases 2-6. This is
the **sixth** judgment-based skill evaluated with self-authored,
single-rater fixtures. All 8 fixtures scored perfect precision/recall on
both layers — stated plainly as *not* evidence of higher judgment quality
than Phase 6's non-perfect score (`root-cause-analyzer`'s case-03,
0.67/0.67); a single self-authored evaluation cannot support that
comparison either way.

**Dogfood run** (`examples/architecture-decision/example-run.md`):
regenerated a fresh `codebase-intelligence` report against this repo's
current (7-skill, 143-module) state, then ran a real decision this phase's
own build actually faced — whether `architecture-decision` should require
or merely accept `codebase-intelligence` composition (the same choice
ADR-013 records). Two real, disclosed findings: (1) a same-session
**found-and-fixed bug** — the tradeoff-detection regex matched only the
noun form "tradeoff"/"trade-off," not the verb phrasing "trades X for Y,"
which the dogfood decision's own text used twice (L20); fixed in
`decision_patterns.py`, all 34 tests and all 8 fixtures re-verified passing
after the fix. (2) A **disclosed, not-fixed limitation** — at full-repo
scale, a decision *about the platform's own architecture* produces a
nearly-uninformative blast-radius signal (both options scored 240+ and
touched all 10 hotspots), because the decision text's vocabulary
unavoidably overlaps this repo's own recurring vocabulary (L21) — a
sharper version of the L14/L19 coincidental-substring limitation.

**Memory-bank updates this phase**: `03-architecture.md` (Pattern 2 reused
a sixth time), `05-evaluation-framework.md` (Architecture Decision Record
Checklist), `11-decisions.md` (ADR-013), `12-known-limitations.md` (L20,
L21, L8 update), `16-assumptions-and-validation.md` (A5, A10 updated),
`08-roadmap.md` (Phase 7 marked complete with a reordering note, Phase 8
now Refactoring Safety), `implementation-status.md`, `07-current-state.md`,
`CHANGELOG.md`, `sprint-history/SPRINT-07.md`, root `README.md`/`ROADMAP.md`/
`QuickStarterGuide.md`/`DEPENDENCIES.md`, `skills/architecture-decision/README.md`
(Status line).

## Open threads / not yet decided

- Phase 8 (Refactoring Safety) is proposed next per [[08-roadmap]] but not
  started and not re-justified against evidence yet — that re-justification
  happens at the start of Phase 8, not now.
- **L8 remains the most important open thread, now applying six times**:
  five of six judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard,
  architecture-decision) scored 100% precision/recall against self-authored
  ground truth; the sixth (root-cause-analyzer) scored 7/8 perfect and 1/8
  at 0.67/0.67 (L19). All outcomes are equally inconclusive about
  real-world quality — self-authored, single-rater evidence either way.
  The inter-rater-agreement experiment (A5) still has not been run for any
  of the six.
- **Experiment A/B and A7's real experiment are all still not viable to run
  for real** — [[17-experiment-viability-check.md]]'s pilots (A, B, C) found
  plausible-but-narrow signal on N=1 each; Phase 7's dogfood run is
  additional real-usage evidence for A10, but a different shape than Phase
  4's/Phase 6's — composition executed correctly but was not decisive on
  the real decision it was used for (L21), an honest data point against
  overclaiming, not for it. None upgrades its assumption's status beyond
  UNKNOWN — the missing ingredient in every case is the same: a real
  second party this session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5), L18 (Phase 6, scope boundary), L21 (Phase 7, disclosed
  keyword-collision-at-scale limitation) remain deliberately deferred —
  revisit only if real usage shows they matter.
- No real (non-agent) engineer has used any of the seven skills yet — Trust
  Status stays EXPERIMENTAL on all seven, and assumptions
  A2/A3/A5/A7/A10 in [[16-assumptions-and-validation]] remain only
  partially evidenced.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `README.md` (root) — primary public-facing entry point
5. `skills/architecture-decision/SKILL.md`,
   `skills/root-cause-analyzer/SKILL.md`,
   `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
6. `examples/architecture-decision/example-run.md` (the real decision run
   that found and fixed L20, and disclosed L21)
7. [[17-experiment-viability-check.md]]
8. `blogs/` — earlier public-facing material (written before Phase 6; not
   yet updated with Phase 6 or Phase 7 posts)

## Last updated

2026-08-23 — end of Phase 7.
