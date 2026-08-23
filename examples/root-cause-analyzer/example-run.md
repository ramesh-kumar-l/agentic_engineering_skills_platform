# Root Cause Analyzer — real dogfood run

Unlike Phases 1–5's synthetic evaluation fixtures, this is a genuine run
against this platform's own current repository state, demonstrating the
required composition with `codebase-intelligence` (ADR-010, reused a second
time per ADR-012) end to end — not a hypothetical.

**Honesty note up front**: this is a *retrospective validation*, not a live
bug discovery. The symptom below describes L16 — a real bug this project
already found and fixed during Phase 5 (`project-memory-bank/
12-known-limitations.md`). The question this run actually answers is
narrower and still genuine: **given only a natural-language bug report (no
stack trace, no hint at the file name), does this skill's candidate scorer
rank the file that was actually the true root cause anywhere near the top?**
That is a fair, non-circular test — the report.json was regenerated fresh
against the repo's current (post-fix, 6-skill) state, and the symptom text
was written the way a real bug reporter would write it, not copied from the
fix commit.

## Step 1 — Regenerate a fresh codebase-intelligence report

```
cd skills/codebase-intelligence
python -m engine.cli <repo-root> --format both --out examples/root-cause-analyzer/ci-report
```

Output: `examples/root-cause-analyzer/ci-report/report.json` (5285 lines),
covering all six skills now in the repo (including this one).

## Step 2 — Run root-cause-analyzer against a real symptom

Symptom (`examples/root-cause-analyzer/symptom.txt`), written the way a bug
reporter would describe L16 without knowing the internal cause:

> Expected security-context-guard to classify this action as
> REQUIRES_HUMAN_APPROVAL, but it returned AUTHORIZE instead. Steps to
> reproduce: run the engine CLI with `--action "Commit and push the new
> Security Context Guard skill files (skills/security-context-guard/,
> evaluations/security-context-guard/, project-memory-bank updates) to the
> shared origin repository."` Error: no exception is raised, but
> `classification.suggested_verdict` comes back `AUTHORIZE` when this is
> clearly a Publishing-category action that should require approval. The
> action-pattern matcher in the security guard's engine seems to require the
> verb and its object keyword to appear close together in the action text,
> and this action's parenthetical file list pushes "push" and "origin" far
> apart — well over a hundred characters.

```
cd skills/root-cause-analyzer
python -m engine.cli examples/root-cause-analyzer/symptom.txt \
  --ci-report examples/root-cause-analyzer/ci-report/report.json \
  --format both --out examples/root-cause-analyzer/output
```

**Symptom flags**: none — the report states expected vs. actual, repro
steps, and an "error" (the misclassification), so all three absence checks
pass.

**Parsed stack frames**: none — this was a silent misclassification, not an
exception, so there was never a traceback to parse. Every candidate below is
therefore keyword-tier, not stack-trace-tier — a real, honest limitation of
this fixture, not a shortcoming hidden from the report.

**Candidate report** (top of 122 scored modules — see
`examples/root-cause-analyzer/output/root-cause-report.md` for the full
list):

| Rank | Path | Score |
|---|---|---|
| 1 | `skills/security-context-guard/engine/action_patterns.py` | 56 |
| 2 | `skills/security-context-guard/tests/test_action_patterns.py` | 41 |
| 3 | `skills/security-context-guard/engine/models.py` | 40 |
| 4 | `evaluations/security-context-guard/run_evaluation.py` | 38 |
| 5 | `skills/security-context-guard/engine/classification.py` | 38 |

`engine/action_patterns.py` — the module that actually contained L16's
fixed-distance proximity-window bug — ranks **first**, purely from keyword
overlap with a natural-language description that never names the file,
never uses the word "proximity," and never mentions the fix. The next
closest thing to it, `classification.py` (where the `suggested_verdict`
field the symptom quotes actually lives), ranks 5th — a plausible
alternative hypothesis, correctly still surfaced in the top 5, not buried.

## Step 3 — Investigate against the Root Cause Investigation checklist (real, not fabricated)

**Symptom restated**: `security-context-guard` under-classifies a real
`Publishing`-category action (commit + push to shared origin) as
`AUTHORIZE` instead of `REQUIRES_HUMAN_APPROVAL`, with no exception raised.

**Reproduction context**: given — a specific `--action` string with a
parenthetical file list between the verb ("push") and its object ("origin").

**Candidate locations**: `action_patterns.py` (top-ranked, keyword tier) —
this is the module responsible for verb+object action-category matching per
its docstring and matched vocabulary ("pattern", "verb", "object", "text",
"parenthetical" all hit). `classification.py` (5th) is a plausible secondary
candidate since it owns the `suggested_verdict` rollup the symptom directly
quotes.

**Evidence tier**: keyword only for every candidate — no stack trace exists
for a silent misclassification, so none of these is confirmed; all are
leads, stated as such rather than presented as diagnosis.

**Blast radius**: `action_patterns.py` has fan_in=1, fan_out=0 — low blast
radius, a leaf pattern-table module. A fix here is unlikely to ripple into
unrelated call sites.

**Recent-change correlation**: N/A — the symptom gives no deploy/release
timing signal.

**Ruled-out candidates**: `test_action_patterns.py` (2nd) and
`test_classification.py` are ruled out as *fix* locations even though they
score highly — a test file scoring high on the same vocabulary as the
module it tests is expected and not itself evidence of where the defect is;
they are the right place to look for a **regression test**, not the root
cause.

**Confirmation step**: read `action_patterns.py`'s matching logic for the
`Publishing` category and check whether it requires the verb and object
keyword within a fixed character window — if so, construct exactly this
symptom's action string as a test input and confirm it fails to match before
touching any code.

**Fix-risk note**: low — `action_patterns.py` has fan_in=1 (only
`scanner.py` depends on it), so a fix is unlikely to have a wide blast
radius; still worth re-running the full `security-context-guard` suite
(58/58) after any change, not just the new regression case.

**Assumption flag**: assuming the defect is in the matching *window/distance
logic* specifically (as the symptom's own final sentence hypothesizes),
rather than in the pattern table's keyword list itself — worth confirming
by reading the matching function's actual implementation before writing a
fix, not treating the symptom reporter's guess as confirmed.

## Outcome

This is real (if retrospective) evidence the required-composition
architecture works for diagnosis, not just planning: a fresh
`codebase-intelligence` report was genuinely necessary and genuinely used,
and the tiered candidate scorer — using keyword overlap alone, with zero
stack-trace evidence available — ranked the true historical root-cause file
first out of 122 scored modules, with the module that actually owns the
misclassified field as a well-ranked (5th) alternative hypothesis rather
than lost in noise. This does not generalize past N=1: it is one retrospective
case where the reporter's natural language happened to share enough
vocabulary with the target module's docstring/tests. A prospective run
against a genuinely new, not-yet-diagnosed bug remains the real test this
project has not yet run — flagged the same way `feature-planner`'s L14 and
`security-context-guard`'s Pilot C were: a real, disclosed, single data
point, not proof of general diagnostic quality.
