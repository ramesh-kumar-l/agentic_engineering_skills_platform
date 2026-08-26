# Candidate Tasks for Usage Comparison

Selection rule: a task only belongs here if it's a genuine task someone
actually has (a real diff to review, a real bug to root-cause, a real
feature to plan) — not a synthetic stand-in written to make a skill look
good. Replace or add to this list with your own real tasks; the ones below
are starting suggestions mapped to an existing skill, not prescribed
choices.

| # | Task (real, not synthetic) | Skill to compare against plain prompting |
|---|---|---|
| 1 | Review a real, currently-open diff in a repo you work in | `adversarial-diff-reviewer` |
| 2 | Root-cause a real bug you're currently investigating | `root-cause-analyzer` |
| 3 | Plan a real, upcoming feature you actually intend to build | `feature-planner` |
| 4 | Assess whether a real, already-open PR is ready to ship | `release-readiness` |
| 5 | Decide whether a real refactor you're considering is safe | `refactoring-safety` |

## Recording a task

For each task you actually run, note here (or in the run log's `notes`
column):
- What the task actually was, in one sentence — specific enough that
  "was this a fair comparison" is checkable later.
- Which repo/codebase it was run against.
- Whether the plain-prompting arm was run *before* seeing the skill's
  output for that same task (required for a fair comparison — see README).
