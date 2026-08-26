# Architecture Decision — real dogfood run

## What this is
A real, in-session use of `architecture-decision` against a real decision
this project's Phase 7 build actually faced: **should `architecture-decision`
require a `codebase-intelligence` report as a hard precondition (reusing
ADR-010 a third time), or treat it as optional (like `security-context-guard`,
ADR-011)?** This is not a synthetic scenario — this decision was made, for
real, while building this skill (see `project-memory-bank/11-decisions.md`
ADR-013). This is a genuine, honest use of the tool, not a demo written to
flatter it.

## Step 1 — regenerate a fresh codebase-intelligence report
`skills/codebase-intelligence/`, run against the whole repo root as it stands
after Phase 6 plus this phase's `skills/architecture-decision/` code:
`python -m engine.cli ../.. --format both --out ../../examples/architecture-decision/ci-report`.
143 modules, 10 hotspots (all `engine/models.py`/`engine/report.py` files —
every skill's central dataclass hub and orchestrator are structurally
central by construction). See `ci-report/report.json`.

## Step 2 — run architecture-decision
`decision.txt` states both options, their tradeoffs (Option A: correctness
over flexibility; Option B: reach over correctness), reversibility (fully
reversible, one-file change), and an explicit "no new security surface"
note. `python -m engine.cli decision.txt --ci-report ci-report/report.json --format both --out output`.
See `output/architecture-decision-report.md` for the full report.

## What the engine found — including a real bug it caught in itself
Two things happened, and both are worth stating plainly.

**First, a real gap this dogfood run found and fixed same-session.** The
first run flagged `no-tradeoff-signal` even though the decision text states
two tradeoffs explicitly: "Option A trades flexibility ... for correctness"
and "Option B trades correctness for reach." `decision_patterns.py`'s
absence regex only matched the noun form (`tradeoff`/`trade-off`), not the
verb form ("trades X for Y") — a real, disclosed false absence-flag, the
same class of gap as `security-context-guard`'s L16 (a real phrasing the
regex table didn't anticipate, found by using the tool on real text, not
synthetic fixtures). Fixed in `engine/decision_patterns.py` by adding
`trades?\b` to the tradeoff pattern; all 34 unit tests and all 8 evaluation
fixtures still pass after the fix (re-verified, not assumed). After the fix,
only `vague-decision-language` fires, on the word "just" in "just without
blast-radius grounding" — a defensible, if borderline, catch: "just" is
being used to minimize what Option B gives up, which is exactly the kind of
framing this pattern exists to flag.

**Second, a real, more serious limitation this run demonstrates but does
NOT fix.** Both options' blast-radius scores are inflated to the point of
being nearly meaningless: Option A scores 241 and touches all 10 hotspots;
Option B scores 256 and touches the same 10 hotspots. This is the
`engine/`-prefix keyword-collision limitation already disclosed in this
skill's own evaluation fixtures (case-01, case-05 — see
`evaluations/architecture-decision/RESULTS.md`), but at full-repository
scale it's far worse than the synthetic fixtures showed: this decision text
is *about* the architecture-decision skill itself, so it necessarily reuses
this project's own vocabulary ("codebase", "intelligence", "report",
"adr", "composition", "decision") — vocabulary that appears in nearly every
file in a 143-module, 7-skill repository that documents its own
architecture obsessively. The result is a blast-radius signal that is
real (every listed module genuinely does contain those words) but not
useful: it cannot distinguish "this decision is about the whole platform"
from "this decision's wording happens to overlap this repo's own
vocabulary everywhere." A keyword-only scorer cannot fix this — it would
need either TF-IDF-style down-weighting of corpus-common terms, or a
minimum keyword-specificity threshold, neither implemented here. Logged as
a new limitation rather than silently accepted.

## Outcome
Option A (required composition) is the real decision this project made —
recorded as ADR-013's precondition in `11-decisions.md`, for the same
"ungrounded output is actively harmful" reason ADR-010 gives. Running the
tool on this exact decision after the fact did not change that outcome
(the deterministic layer's blast-radius signal was too noisy to be
decisive either way at this scale — see the limitation above), but the
anti-pattern scan did catch one real, fixable gap in the tool itself before
it shipped. This is N=1, self-run, single-session evidence — not proof this
skill improves real architecture decisions, and not the inter-rater
experiment `project-memory-bank/16-assumptions-and-validation.md` (A5)
still calls for. It is, however, a genuine use of the tool on a real
decision with a real, disclosed outcome (one bug found and fixed, one
limitation found and left honestly documented), which is the same bar every
prior phase's dogfood run has been held to.
