# Quick Starter Guide

Everything a first-time visitor needs to clone this repo, understand what
it is, run a skill end to end, run the tests, and know where to go next.
If you only read one document besides the README, read this one.

## 1. What is this, in 30 seconds?

This repo is a portfolio of **AI coding-agent "skills"** — not prompts.
Each skill is a `SKILL.md` contract (intent, inputs, workflow, security
constraints, evaluation, known limitations) backed by a small, tested,
stdlib-only Python engine. Nine exist today, all `Trust Status:
EXPERIMENTAL`, all tested, all evaluated, all honestly documented — see
[`README.md`](README.md) for the full picture and
[`project-memory-bank/`](project-memory-bank/) for the complete project
history and reasoning.

You do not need an AI agent, an API key, or an internet connection to run
any of this. Every skill's deterministic engine is a normal Python CLI you
can run yourself, right now, from a terminal.

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

skills/                       The nine skills — the actual product
  codebase-intelligence/
  adversarial-diff-reviewer/
  acceptance-test-engineer/
  feature-planner/
  security-context-guard/
  root-cause-analyzer/
  architecture-decision/
  refactoring-safety/
  regression-hunter/

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
skill, including the two skills that take extra input
(`acceptance-test-engineer` wants a requirement, `feature-planner` **requires**
a `codebase-intelligence` report — see below).

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

Expect **342 passing tests** across all nine skills (24 + 23 + 24 + 21 + 58 + 32 + 34 + 62 + 64)
as of the most recent phase. See
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

This regenerates `RESULTS.md` with real, current scores. For the four
judgment-based skills (everything except `codebase-intelligence`), the
harness scores two separate layers — a fully automated deterministic layer,
and a judgment layer comparing an AI agent's actual derivation against
ground truth. **Read the top of any `RESULTS.md` before trusting the
number** — every one of them discloses the same honest caveat: the scores
are self-authored/single-rater evidence, not proof of real-world quality.
This is not a footnote to skim past — it's one of the more interesting
engineering decisions in this repo. See
[Your AI Eval Says 100%. That Should Worry You.](blogs/04-your-ai-eval-says-100-percent.md)

## 7. Composing two skills together

`feature-planner` is the one skill that **requires** another skill's output
as a hard precondition (not optional context) — see
[ADR-010](project-memory-bank/11-decisions.md):

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

## 8. Where to read next, depending on what you want

| You want to... | Read this |
|---|---|
| Understand the whole project's philosophy and status | [`README.md`](README.md) |
| See exactly what's built vs. what's planned | [`project-memory-bank/implementation-status.md`](project-memory-bank/implementation-status.md) |
| Understand one specific skill deeply | `skills/<name>/SKILL.md` |
| See a skill run against a real (not synthetic) problem | `examples/<name>/example-run.md` |
| Understand the two architecture patterns used across all nine skills | [`project-memory-bank/03-architecture.md`](project-memory-bank/03-architecture.md), or the more readable [blog version](blogs/02-two-architectures-for-ai-agent-skills.md) |
| See every real bug found and fixed via dogfooding | [`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md), or the [blog version](blogs/03-i-dogfooded-every-skill-i-built.md) |
| Understand what's actually validated vs. still assumed | [`project-memory-bank/16-assumptions-and-validation.md`](project-memory-bank/16-assumptions-and-validation.md) |
| Propose a new skill | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Report a security issue | [`SECURITY.md`](SECURITY.md) |
| See what's next | [`ROADMAP.md`](ROADMAP.md) |

## 9. FAQ

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
seriously (five were found and fixed via dogfooding already — see
[`project-memory-bank/12-known-limitations.md`](project-memory-bank/12-known-limitations.md)).
