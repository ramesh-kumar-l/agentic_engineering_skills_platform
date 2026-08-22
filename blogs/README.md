# Blog series: Building the Agentic Engineering Skills Platform

Five posts, written as the project was actually built — not a retrospective
marketing pass. Every code snippet, test count, and bug described here is
real and traceable to a specific file in this repository at the time of
writing. Where a claim is uncertain or unproven, the post says so explicitly,
the same way the project's own [`project-memory-bank/`](../project-memory-bank/)
does.

## Reading order

Each post stands alone, but they build on each other in this order:

1. **[A Skill Is Not a Prompt](01-a-skill-is-not-a-prompt.md)** — why this
   project exists, and the contract model (`SKILL.md`) it's built around.
2. **[Two Architectures for AI Agent Skills](02-two-architectures-for-ai-agent-skills.md)**
   — the deterministic-engine + agent-judgment split used across four of
   five skills, and why baking judgment into regex would be dishonest.
3. **[I Dogfooded Every Skill I Built](03-i-dogfooded-every-skill-i-built.md)**
   — five real bugs, found by using each skill on real work instead of only
   synthetic fixtures, with the actual before/after code.
4. **[Your AI Eval Says 100%. That Should Worry You.](04-your-ai-eval-says-100-percent.md)**
   — why four perfect evaluation scores in a row are a methodology warning
   sign, not a trophy, and what real evidence would look like instead.
5. **[Building an AI Agent That Can't Authorize Its Own Actions](05-building-an-ai-agent-that-cant-authorize-its-own-actions.md)**
   — a full walkthrough of `security-context-guard`'s classify → minimize →
   sanitize → authorize → execute → audit workflow, and the hard rule that
   the engine never gets to make the authorization call itself.

## A note on the Mermaid diagrams

Every post includes Mermaid diagrams as fenced ` ```mermaid ` code blocks.
GitHub renders these natively — if you're reading this in the repo, they'll
just work. Medium's editor does not render Mermaid natively; when
cross-posting, export each diagram as an image first (e.g. via
[mermaid.live](https://mermaid.live)) and embed it as a normal image in the
Medium draft. The source stays here as the single source of truth either
way.

## Why these posts exist

The goal is to document real engineering decisions — including the ones that
turned out to be mistakes, caught by the project's own dogfooding discipline
— clearly enough that another engineer could learn something concrete from
them, and honestly enough that the claims hold up under scrutiny. If you
find an error or a claim that doesn't check out, that's exactly the kind of
feedback this project's [`CONTRIBUTING.md`](../CONTRIBUTING.md) asks for.
