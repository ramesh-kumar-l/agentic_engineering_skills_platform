# Quick Starter Guide

Everything a first-time visitor needs to clone this repo, understand what
it is, run a skill end to end, run the tests, and know where to go next.
If you only read one document besides the README, read this one.

## 1. What is this, in 30 seconds?

This repo is a portfolio of **AI coding-agent "skills"** — not prompts.
Each skill is a `SKILL.md` contract (intent, inputs, workflow, security
constraints, evaluation, known limitations) backed by a small, tested,
stdlib-only Python engine. Fifteen exist today — the originally-scoped
portfolio is now complete — all `Trust Status: EXPERIMENTAL`, all tested,
all evaluated, all honestly documented — see
[`README.md`](README.md) for the full picture and
[`project-memory-bank/`](project-memory-bank/) for the complete project
history and reasoning.

You do not need an AI agent, an API key, or an internet connection to run
any of this. Every skill's deterministic engine is a normal Python CLI you
can run yourself, right now, from a terminal.

A second, newer set of six packages at the repo root (`evidence/`,
`project_intelligence/`, `test_strategy/`, `scenario_planner/`,
`test_generation/`, `test_validation/`) forms the **Test Engineering
Platform** — a pipeline that decides which changed files need a test, plans
scenarios, and actually executes agent-authored tests against a real
target repo. See §8 below to run it end to end.

## 2. Prerequisites

| Requirement | Why |
|---|---|
| Python 3.10+ | every skill's engine requires it (`X \| None` union syntax, dataclasses) |
| Git | to clone the repo, and for `adversarial-diff-reviewer` to produce diffs |
| A terminal | bash, zsh, or PowerShell all work — commands below are POSIX-flavored, PowerShell equivalents are one substitution away |

Check your Python version:

```bash
python --version   # or: python3 --version
```

Nothing else is required. See [`DEPENDENCIES.md`](DEPENDENCIES.md) for the
full explanation of why the dependency list is this short (it's
deliberate — [ADR-006](project-memory-bank/11-decisions.md)).

## 3. Clone and orient yourself

```bash
git clone <this-repository-url>
cd agentic_engineering_skills_platform
```

Top-level layout:

```
README.md                    Start here for the big picture
QuickStarterGuide.md          This file
DEPENDENCIES.md               What's installed and why
ROADMAP.md                    Where the project is headed (pointer file)
CHANGELOG.md                  What shipped, phase by phase
CONTRIBUTING.md               How to propose a skill
SECURITY.md                   How to report a vulnerability
LICENSE                       Apache 2.0

skills/                       The fifteen skills — the actual product
  codebase-intelligence/
  adversarial-diff-reviewer/
  acceptance-test-engineer/
  feature-planner/
  security-context-guard/
  root-cause-analyzer/
  architecture-decision/
  refactoring-safety/
  regression-hunter/
  release-readiness/
  dependency-supply-chain/
  engineering-knowledge-capture/
  context-optimizer/
  workflow-composer/
  engineering-memory/

evidence/                     TEP pipeline: wraps any skill's CLI run, records provenance
project_intelligence/         TEP pipeline: derives a TestEnvironmentProfile
test_strategy/                TEP pipeline: decides which changed files need a test
scenario_planner/             TEP pipeline: turns flagged targets into test scenarios
test_generation/               TEP pipeline: produces a deterministic test-generation plan
test_validation/               TEP pipeline: executes agent-authored tests, records pass/fail

evaluations/                  Per-skill evaluation harnesses + fixtures + RESULTS.md
examples/                     Real "dogfood" runs — each skill used on real work, not synthetic demos
blogs/                        Deep-dive technical write-ups on how/why this was built
project-memory-bank/          The project's own working memory — vision, architecture,
                               decisions, known limitations, assumptions, current state
```

Every skill directory has the same internal shape:

```
skills/<skill-name>/
  SKILL.md          the actual contract — read this to understand the skill
  README.md         quickstart commands for this one skill
  pyproject.toml     dependency/test config
  engine/            the deterministic Python backing tool
  tests/             unit + integration tests
```

## 4. Run your first skill (5 minutes)

`codebase-intelligence` is the simplest starting point — point it at any
repository (including this one) and it produces a structural map: files,
imports, definitions, a dependency graph, and hotspot ranking.

```bash
cd skills/codebase-intelligence
python -m engine.cli ../.. --format markdown
```

That runs the engine against the whole platform repo and prints a Markdown
report to stdout. Add `--out some/dir` to write `report.json` and
`report.md` to disk instead of printing.

Try the adversarial diff reviewer's engine next (this one needs a diff to
look at — make a small edit first, or just diff against nothing to see the
"no changes" path):

```bash
cd ../adversarial-diff-reviewer
git diff | python -m engine.cli - --format markdown
```

Every skill's own `README.md` has the exact copy-pasteable command for that
skill. Most take extra input beyond a bare repo path — `acceptance-test-
engineer` wants a requirement, and eleven skills (`feature-planner`
through `engineering-memory`) **require** a `codebase-intelligence`
report as a hard precondition, not optional context — see §7 below.

**Important distinction**: the CLI you just ran is only *half* of a skill.
It produces a deterministic "pre-processing packet" (stats + flags) — the
actual judgment (the code review, the acceptance-case derivation, the plan,
the security recommendation) is performed by an AI agent following that
skill's `SKILL.md` workflow, using the CLI's output as a grounded starting
point rather than reasoning about raw, unstructured input. Running the CLI
alone shows you the leads; it is not the whole skill. See
[Two Architectures for AI Agent Skills](blogs/02-two-architectures-for-ai-agent-skills.md)
in the blog series for why this split exists.

## 5. Run the tests

Every skill is independently testable:

```bash
cd skills/codebase-intelligence
pip install -e ".[dev]"
pytest
```

Repeat per skill, or run everything from the repo root:

```bash
for d in skills/*/; do
  echo "=== $d ==="
  (cd "$d" && pip install -e ".[dev]" -q && pytest -q)
done
```

Expect **733 passing tests** across all fifteen skills (42 + 29 + 24 + 21 + 58 + 32 + 34 + 65 + 70 + 84 + 55 + 47 + 64 + 51 + 57)
as of the most recent change. The same loop works for the 6 Test
Engineering Platform packages at the repo root (`for d in evidence
project_intelligence test_strategy scenario_planner test_generation
test_validation; do (cd "$d" && pip install -e ".[dev]" -q && pytest -q);
done`) — expect **166 passed, 3 skipped** (see §8 below for what these
packages do). See
[`project-memory-bank/implementation-status.md`](project-memory-bank/implementation-status.md)
for the current authoritative count.

## 6. Run an evaluation harness

Every skill ships with an evaluation harness scoring it against
hand-authored fixtures — this is what backs the "Evaluated" claim in each
skill's maturity level (see
[`project-memory-bank/04-skill-contract.md`](project-memory-bank/04-skill-contract.md)):

```bash
cd evaluations/codebase-intelligence
python run_evaluation.py
```

This regenerates `RESULTS.md` with real, current scores. For the fourteen
judgment-based skills (everything except `codebase-intelligence`, which is
fully deterministic), the harness scores two separate layers — a fully
automated deterministic layer, and a judgment layer comparing an AI
agent's actual derivation against ground truth. **Read the top of any
`RESULTS.md` before trusting the number** — every one of them discloses
the same honest caveat: the scores are self-authored/single-rater
evidence, not proof of real-world quality.
This is not a footnote to skim past — it's one of the more interesting
engineering decisions in this repo. See
[Your AI Eval Says 100%. That Should Worry You.](blogs/04-your-ai-eval-says-100-percent.md)

## 7. Composing two skills together

`feature-planner` was the first skill to **require** another skill's
output as a hard precondition (not optional context) — see
[ADR-010](project-memory-bank/11-decisions.md). That rule has since been
reused by ten more skills (`root-cause-analyzer` through
`engineering-memory`); every one of them needs a real
`codebase-intelligence` report before it will run. The same manual
two-step pattern shown below works for any of them — just swap the
second command for the skill you want:

```bash
# 1. Generate a codebase-intelligence report first (required)
cd skills/codebase-intelligence
python -m engine.cli /path/to/repo --format json --out /path/to/ci-out

# 2. Feed it into feature-planner alongside a task description
cd ../feature-planner
echo "Add a --verbose flag to the CLI." | \
  python -m engine.cli - --ci-report /path/to/ci-out/report.json --format both --out /path/to/output-dir
```

Without a valid `report.json`, the command above exits non-zero with an
actionable error — it does not silently degrade. `security-context-guard`
also accepts an optional `--ci-report` flag, but treats a missing one as a
warning, not a failure — the difference between those two design choices is
itself documented (ADR-010 vs ADR-011 in
[`project-memory-bank/11-decisions.md`](project-memory-bank/11-decisions.md)).

Two later skills compose differently, worth knowing about:
- `workflow-composer` automates the two-step pattern above instead of you
  running it by hand — it subprocess-invokes a named template's real
  steps (e.g. `codebase-intelligence` → `feature-planner`) and fails
  closed if a step breaks or a compatibility check fails. See its own
  `README.md` for the exact command.
- `engineering-memory` composes on a `codebase-intelligence` report the
  same required way, but retrieves against *this project's own*
  `project-memory-bank/` markdown rather than a target repo's code — the
  first "self-referential" skill in the portfolio.

## 8. Running the Test Engineering Platform pipeline end-to-end

Six more packages at the repo root (`evidence/`, `project_intelligence/`,
`test_strategy/`, `scenario_planner/`, `test_generation/`,
`test_validation/`) form a second pipeline: given a target repo and a real
git diff, it decides which changed files need a test, plans scenarios,
produces a deterministic plan for an agent to write tests from, then
actually **runs** those agent-authored tests — this platform's only
execution capability. Unlike the fifteen skills above, most of these
packages' CLIs are invoked from the **repo root**, not from inside the
package directory, and each one's input is the previous one's JSON output:

```bash
# 1. codebase-intelligence and regression-hunter (existing skills) produce
#    the two starting reports this pipeline builds on
cd skills/codebase-intelligence
python -m engine.cli /path/to/target-repo --format json --out /path/to/ci-out
cd ../regression-hunter
git -C /path/to/target-repo diff <base>..<head> | \
  python -m engine.cli - --ci-report /path/to/ci-out/report.json --format json --out /path/to/rh-out

# 2. derive a TestEnvironmentProfile from the codebase-intelligence report
cd ../..
python -m project_intelligence.cli /path/to/ci-out/report.json --out /path/to/tep-out

# 3. decide which changed files need a test
python -m test_strategy.cli /path/to/rh-out/report.json /path/to/tep-out/test-environment-profile.json --out /path/to/tep-out

# 4. plan candidate test scenarios for each flagged target
python -m scenario_planner.cli /path/to/tep-out/test-strategy-report.json /path/to/rh-out/report.json /path/to/ci-out/report.json --out /path/to/tep-out

# 5. produce a deterministic generation plan (an agent writes the actual
#    test files from this plan — no engine here authors code)
python -m test_generation.cli /path/to/tep-out/scenario-plan-report.json /path/to/target-repo --out /path/to/tep-out

# 6. once an agent has written files into, say, /path/to/generated-tests/,
#    actually execute them and record real pass/fail evidence
python -m test_validation.cli /path/to/generated-tests /path/to/tep-out/test-environment-profile.json /path/to/target-repo --out /path/to/tep-out
```

A real, non-synthetic run of this exact chain is committed at
`examples/test-validation/example-run.md` (and the individual
`examples/<tep-pkg>/example-run.md` for each earlier stage) — read those
before running it yourself against an unfamiliar repo. `test_validation`
has no sandboxing beyond a per-file timeout, path-containment checks, and
file-count/size caps — see
[`project-memory-bank/25-tep-pipeline-overview.md`](project-memory-bank/25-tep-pipeline-overview.md)
for the full pipeline diagram and
[ADR-029/ADR-030](project-memory-bank/11-decisions.md) for exactly what is
and isn't bounded.

## 9. Where to read next, depending on what you want

| You want to... | Read this |
|---|---|
| Understand the whole project's philosophy and status | [`README.md`](README.md) |
| See exactly what's built vs. what's planned | [`project-memory-bank/implementation-status.md`](project-memory-bank/implementation-status.md) |
| Understand one specific skill deeply | `skills/<name>/SKILL.md` |
| See a skill run against a real (not synthetic) problem | `examples/<name>/example-run.md` |
| Understand the two architecture patterns used across all fifteen skills | [`project-memory-bank/03-architecture.md`](project-memory-bank/03-architecture.md), or the more readable [blog version](blogs/02-two-architectures-for-ai-agent-skills.md) |
| See every real bug found and fixed via dogfooding | [`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md), or the [blog version](blogs/03-i-dogfooded-every-skill-i-built.md) |
| Understand what's actually validated vs. still assumed | [`project-memory-bank/16-assumptions-and-validation.md`](project-memory-bank/16-assumptions-and-validation.md) |
| Understand the Test Engineering Platform pipeline | [`project-memory-bank/25-tep-pipeline-overview.md`](project-memory-bank/25-tep-pipeline-overview.md), or §8 above |
| Propose a new skill | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Report a security issue | [`SECURITY.md`](SECURITY.md) |
| See what's next | [`ROADMAP.md`](ROADMAP.md) |

## 10. FAQ

**Do I need Claude, GPT, or any specific AI agent to use this?**
No, not to run the engines or tests — those are plain Python. To actually
*use* a skill as intended (its full `SKILL.md` workflow, including the
agent-driven judgment steps), you need an AI coding agent that can read a
`SKILL.md` file and follow it; the format is intentionally
runtime-agnostic Markdown, not tied to one vendor (see
[ADR-002](project-memory-bank/11-decisions.md)).

**Why "EXPERIMENTAL" on every skill? Is this not finished?**
Trust status is evidence-based, not a marketing label — see
[`project-memory-bank/04-skill-contract.md`](project-memory-bank/04-skill-contract.md)'s
trust model. Every skill here is tested and evaluated on its own synthetic
fixtures, but none has been used by a real engineer other than this
project's own author yet, and every judgment-based skill's 100% evaluation
score is self-authored (see Q below). "EXPERIMENTAL" is the honest label
until that changes — this project explicitly bans unsupported reliability
claims (NFR4 in
[`project-memory-bank/02-requirements.md`](project-memory-bank/02-requirements.md)).

**Why does every evaluation say "100% precision/recall" but also say not to
trust it?**
Because the same agent session wrote the fixtures, the expected answers,
*and* the actual derivation for each judgment-based skill. A perfect score
under those conditions shows the workflow runs and is internally
consistent — it cannot show real-world quality, because there was no
independent party involved anywhere in the loop. Not every skill actually
scores 100%, either — `root-cause-analyzer` scored 7/8 fixtures perfect and
1/8 at 0.67/0.67, left exactly as computed rather than adjusted to look
better. This is disclosed explicitly everywhere the number appears, not
discovered by a critic later. See
[known limitation L8](project-memory-bank/12-known-limitations.md) and
the [dedicated blog post](blogs/04-your-ai-eval-says-100-percent.md).

**Can a skill's engine deploy to production / delete something / push to
git by itself?**
No. Every engine is read-only and produces a report; nothing in this repo
executes a mutating action against your system, your repo, or any external
service. `security-context-guard` goes further and makes this a hard
architectural rule (not just a convention) — its engine's recommendation is
always advisory; only a human, via the agent's workflow, makes an actual
authorization decision (see [ADR-011](project-memory-bank/11-decisions.md)).

**Where's the roadmap / what's coming next?**
[`ROADMAP.md`](ROADMAP.md) at the root is a short pointer to the full,
living roadmap in
[`project-memory-bank/08-roadmap.md`](project-memory-bank/08-roadmap.md).
The roadmap is explicitly adaptive — a planned phase is not built just
because it's next on a list; each phase is re-justified against evidence
before it starts.

**Something doesn't work as documented — what do I do?**
Please open an issue with input/expected/actual behavior — see
[`CONTRIBUTING.md`](CONTRIBUTING.md#reporting-issues). Real bugs found this
way are exactly the kind of evidence this project is built to take
seriously — a growing number have already been found and fixed (or
honestly disclosed, not fixed) via dogfooding; see
[`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md)
for the current, authoritative list rather than a count repeated here that
would go stale with every new phase.
