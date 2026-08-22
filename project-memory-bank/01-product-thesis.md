# 01 — Product Thesis

## The working thesis (UNPROVEN — see [[16-assumptions-and-validation]])

> AI coding agents are becoming increasingly capable, but engineers and
> organizations lack standardized, reusable, evaluated, secure, and trustworthy
> engineering capabilities for those agents.

This is a hypothesis this project must actively try to falsify, not a foregone
conclusion to build toward. Never force reality to fit the roadmap — if evidence
contradicts the thesis or an assumption under it, update [[08-roadmap]].

## The transformation the platform should enable

```
Vague Engineering Task → Explicit Requirements → Relevant Context →
Structured Plan → Bounded Agent Execution → Tests → Diff Review →
Security Review → Evidence → Human Decision → Engineering Knowledge →
Future Improvement
```

Intended improvements: engineering velocity, correctness, developer leverage,
security, consistency, knowledge reuse, AI-agent reliability, engineering decision
quality.

## Primary success metric

**Time-to-Correct-Result**, not lines of generated code, prompt count, token usage,
agent-action count, or raw automation percentage. See [[15-metrics]] (not yet
created — will be added once there is real usage to measure).

## Target users

**Primary** (design for these first): AI-native software engineers; senior, staff,
and principal engineers; developer productivity teams; platform engineering teams;
AI engineering teams.

**Secondary**: engineering managers; open-source maintainers; enterprise
engineering orgs; AI tooling vendors; engineering educators.

Do not build enterprise administration prematurely — optimize for the individual
engineer first.

## Build-order strategy

```
Skills → Real usage → Evaluation → Repeatability → Community validation →
Composition → Registry → Hosted platform → Enterprise capabilities
```

The repository and its skills **are** the MVP. Do not build a SaaS platform now.

## Validation experiments planned (not yet run)

- **Experiment A** — engineer + normal AI workflow vs. engineer + skill, on real
  tasks, measuring Time-to-Correct-Result, defects, rework, review findings, test
  quality, satisfaction.
- **Experiment B** — normal AI vs. individual skill vs. composed workflow, to test
  whether composition actually adds value.
- **Experiment C** — hand a skill to an external engineer with no explanation;
  observe comprehension, execution, confusion points, failure modes.

None of these have been run yet. First milestone is **3 genuinely useful,
evaluated skills used on real engineering work** — not 15 `SKILL.md` files.
