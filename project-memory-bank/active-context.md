# Active Context

What's in flight right now. Read this first when resuming work — it's the
fastest way to know "what was I in the middle of." Replaced each time, not
appended to. Complements [[implementation-status.md]] (what's built) and
[[07-current-state]] (whole-repo snapshot).

## Current phase

Phase 5 (security-context-guard) — COMPLETE. Phase 6 not started, still
waiting on explicit user instruction per [[08-roadmap]]'s phase protocol.

**Since Phase 5 completed**, a documentation/developer-experience pass was
done at the user's explicit request — this is deliberately **not** Phase 6
and does not consume a phase slot. It touches packaging clarity,
onboarding docs, and public-facing writing, not skill implementation. See
"What just happened" below.

## What just happened (documentation & developer-experience pass)

The user asked for four things, none of which are new skill work: (1)
confirm and document the project's actual dependency footprint, (2) a
comprehensive quickstart for a first-time reader, (3) a production-grade
root `README.md` that answers a newbie engineer's questions without them
needing to read the whole memory bank first, (4) a 5-post technical blog
series under `/blogs/` for external publication (Medium + GitHub
visibility), explicitly framed by the user as a hiring-signal artifact for
senior/FAANG audiences. Also requested: refresh each skill's own
`README.md` with current status, and keep the memory bank's "save state"
discipline current through this pass, same as every phase.

**New root files**:
- `requirements.txt` — the one real dependency (`pytest>=7.0`); documents
  that this is intentional, not incomplete.
- `DEPENDENCIES.md` — full explanation of the zero-runtime-dependency
  choice (ties back to ADR-006), per-skill `pyproject.toml` shape, install
  options, non-Python tooling needed (git only).
- `QuickStarterGuide.md` — prerequisites, clone, first-skill walkthrough,
  test/evaluation-harness instructions, composition example
  (`feature-planner` + `codebase-intelligence`), a "where to read next"
  table, and an FAQ addressing the questions most likely to come up
  (do I need an AI agent to run this, why EXPERIMENTAL everywhere, why do
  100% eval scores come with a warning, can any engine self-execute a
  risky action).
- `README.md` — fully rewritten (previous version was a short pointer
  file). Now covers the capability-progression mermaid diagram, the
  five-skill table, a runnable quickstart, both architecture patterns with
  a mermaid data-flow diagram, an explicit "Evaluation & Honesty" section
  surfacing the L8 self-grading caveat prominently rather than leaving it
  for the memory bank to disclose alone, a table of the five real bugs
  found via dogfooding, and links into the new blog series.

**New `/blogs/` directory** — five posts plus an index `README.md`,
verified against real code/data before writing (`classification.py`,
`action_patterns.py`, `risk_scanner.py`, real `RESULTS.md` numbers, ADR-011,
ADR-009, Pilot C) rather than reconstructed from memory:

1. `01-a-skill-is-not-a-prompt.md` — the contract model, why prompts can't
   carry what a skill needs to carry.
2. `02-two-architectures-for-ai-agent-skills.md` — Pattern 1 vs Pattern 2,
   the "6 of 8 fixtures have zero deterministic flags" evidence for why the
   split earns its complexity, and the ADR-010-vs-ADR-011 optional/mandatory
   composition contrast.
3. `03-i-dogfooded-every-skill-i-built.md` — L1, L5/L6, L10, L13, L16 told
   as one continuous narrative with real before/after code, ending in a
   summary table.
4. `04-your-ai-eval-says-100-percent.md` — the self-grading trap, framed
   around the real four-for-four 100% precision/recall pattern, what an
   inter-rater-agreement experiment would actually require, and Pilot C's
   honestly-neutral result as a second instance of the same discipline.
5. `05-building-an-ai-agent-that-cant-authorize-its-own-actions.md` — the
   Classify→Minimize→Sanitize→Authorize→Execute→Audit workflow, real
   `classification.py` code, ADR-011, and the L16 finding retold in the
   security-specific frame (a security skill's own dogfood run finding a
   bug in itself, not a different skill, for the first time).

Each post includes Mermaid diagrams (flowcharts/sequence diagrams) that
render natively on GitHub; `blogs/README.md` notes that Medium needs them
exported as images first (e.g. via mermaid.live) since Medium doesn't
render Mermaid natively.

**Updated files**: all five `skills/*/README.md` now carry a `**Status**`
line with current test counts, trust status, relevant ADR references, and
(where applicable) a link to the relevant blog post — kept short,
consistent with this repo's existing quickstart-style skill READMEs, not
expanded into full docs.

No code, tests, `SKILL.md` contracts, or evaluation harnesses were touched
in this pass — it is documentation and public-facing writing only. Test
count and evaluation results are unchanged: **149/149 tests passing**,
**five evaluation harnesses**, all previously-reported scores untouched.

## Open threads / not yet decided

- Phase 6 (Root Cause Analyzer) is proposed next per [[08-roadmap]] but
  not started and not re-justified against evidence yet — that
  re-justification happens at the start of Phase 6, not now.
- **L8 remains the most important open thread, now applying four times**:
  all four judgment-based skills (adversarial-diff-reviewer,
  acceptance-test-engineer, feature-planner, security-context-guard) score
  100% precision/recall against self-authored ground truth. This is now
  surfaced prominently in the public-facing README and its own dedicated
  blog post, not just the memory bank — the documentation pass treated this
  as a feature of the project's honesty discipline worth explaining, not a
  weakness to downplay.
- **Experiment A/B and A7's real experiment are all still not viable to run
  for real** — [[17-experiment-viability-check.md]]'s pilots (A, B, and C)
  found plausible-but-narrow signal on N=1 each. None upgrades its
  assumption's status beyond UNKNOWN — the missing ingredient in every case
  is the same: a real second party this session cannot supply for itself.
- L2/L3/L4 (Phase 1), L7/L9 (Phase 2), L11/L12 (Phase 3), L14/L15 (Phase 4),
  L17 (Phase 5) scope boundaries remain deliberately deferred — revisit
  only if real usage shows they matter.
- No real (non-agent) engineer has used any of the five skills yet — Trust
  Status stays EXPERIMENTAL on all five, and assumptions A2/A3/A5/A7/A10 in
  [[16-assumptions-and-validation]] remain only partially evidenced. The
  new blog series and production README are, if anything, the first real
  attempt to get this project in front of external readers at all — a
  precondition for A1/A9 ever moving off UNKNOWN, not evidence toward them
  yet.

## If resuming this session cold, read in this order

1. This file
2. [[implementation-status.md]]
3. [[07-current-state]]
4. `README.md` (root) — now the primary public-facing entry point
5. `skills/security-context-guard/SKILL.md`, `skills/feature-planner/SKILL.md`,
   `skills/acceptance-test-engineer/SKILL.md`,
   `skills/adversarial-diff-reviewer/SKILL.md`, `skills/codebase-intelligence/SKILL.md`
6. `examples/security-context-guard/example-run.md` (the L16 finding + Pilot C)
7. [[17-experiment-viability-check.md]]
8. `blogs/` — the same material as 4-6 above, written for an external reader

## Last updated

2026-08-23 — documentation & developer-experience pass, after Phase 5.
