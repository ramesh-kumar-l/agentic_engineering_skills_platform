# Usage Comparison Harness

Measures the one thing this project has never measured, across ten phases:
does using a skill actually save tokens/turns/time versus plain prompting on
the same real task? Every other harness in `evaluations/` scores a skill
against itself (does its output match hand-authored ground truth). This one
compares a skill **against not using it at all**.

## Why this exists

`project-memory-bank/16-assumptions-and-validation.md`'s A2 ("skills provide
measurable benefit over normal prompting") has stayed `UNKNOWN` since Phase 1
— not because it was forgotten, but because Experiment A (the thing that
would actually test it) was never run, not even once, not even informally.
This harness is the minimum viable version of that experiment: a place to
log real runs and see the numbers, not another architectural argument for
why it *should* be true.

## Honesty caveats — read this before trusting any numbers this produces

- **This is a self-run pilot, not a rigorous experiment.** Same discipline
  as Pilot A/B/C in `project-memory-bank/17-experiment-viability-check.md`
  (governed by ADR-009): N is small, the same person runs both arms, and
  there is no blinding. A result here is a real data point, not proof.
- **Token counts are approximate.** No agent session can precisely
  self-meter its own token consumption after the fact. Real numbers should
  come from the agent client's own usage reporting (e.g. Claude Code's
  per-turn token/cost display), logged manually into the run log — not
  estimated or fabricated by an agent filling in the log itself.
- **"Plain prompting" is not a fair fight if it's run by someone who
  already knows the skill's answer.** Whoever runs the `plain_prompting`
  arm should attempt the task the way they normally would *before* having
  seen the skill's structured output for that same task, not reconstruct it
  afterward.
- **This harness ships empty.** No results are pre-filled, no numbers are
  claimed in this README. `A2`'s status does not change until real runs are
  logged — see `template-run-log.csv`.

## How to use it

1. Pick 2-5 real tasks from `tasks.md` (or add your own real ones — not
   synthetic).
2. For each task, run it twice: once using the relevant skill's full
   workflow, once with plain prompting to the same agent, no skill
   scaffolding. Do the plain-prompting arm on a task you haven't already
   seen the skill's answer for.
3. Log both runs in a copy of `template-run-log.csv` — turns taken,
   approximate tokens (from your agent client's own reporting), wall-clock
   time, and whether the outcome was actually correct/useful.
4. Run `python run_comparison.py <your-log>.csv` to print a summary table.
5. Update `project-memory-bank/16-assumptions-and-validation.md`'s A2 entry
   with what you actually found — including if the result is unflattering.

## What this harness deliberately does not do

- Does not score "quality" — that's a judgment call for whoever reviews the
  two outputs, not something `run_comparison.py` decides.
- Does not aggregate across unrelated task types as if they were
  comparable — the summary table breaks down per task, not just an overall
  average, because a 5-line fix and a full feature plan don't belong in the
  same number.
- Does not run itself — there is no way to automatically generate the
  "plain prompting" baseline without a human actually doing it that way.
