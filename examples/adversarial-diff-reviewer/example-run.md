# Example run — dogfooding against a real diff from this session

Unlike `examples/codebase-intelligence/`, which dogfoods against the whole
platform repo, this example dogfoods against one specific **real, non-
synthetic diff**: the actual fix made to `engine/risk_scanner.py` earlier in
this same Phase 2 session (`dogfood.diff`), reconstructed line-for-line from
the real before/after content. This satisfies the "real diffs" half of the
Phase 2 exit criteria, alongside the 8 synthetic fixtures in
`evaluations/adversarial-diff-reviewer/`.

## What the diff does

Changes `risk_scanner.scan()` from computing `matched_text` for a risk flag
without touching the underlying line content, to redacting the matched span
of `redact=True` patterns (secrets) both in the flag *and* in the raw
`line.content` — because the raw diff content is also part of this engine's
JSON/Markdown output, and leaving the literal secret there would defeat the
point of redacting it in the flag.

## Step 1 — Engine output

```
cd skills/adversarial-diff-reviewer
python -m engine.cli ../../examples/adversarial-diff-reviewer/dogfood.diff --format both
```

Result: 1 file touched, +16/-3 lines, 1 hunk, **zero risk flags**. Correctly
so — neither the before nor after version of this diff contains an actual
secret literal; the defect here is in redaction *logic*, not content shape,
so no regex pattern should fire. This is expected behavior, not a gap: it is
exactly why Step 3 (agent judgment) exists as a separate layer from Step 1.

## Step 2 — Read for context

The full file was read (`skills/adversarial-diff-reviewer/engine/risk_scanner.py`
at the time of review) to understand `PATTERNS` and how `RiskFlag.matched_text`
is consumed downstream by the renderers.

## Step 3 — Adversarial review

Going through the failure-first checklist: the new code redacts the *first*
matched span of a pattern via `pattern.regex.search()` + string slicing, then
writes the redacted result back onto `line.content`. Adversarially asking "what
if this line has the pattern twice?" — e.g.
`api_key = "AAA"; token = "BBB"` both match the single `hardcoded-secret`
pattern (it alternates `api_key|...|token|...`). `search()` only finds the
**first** occurrence; the second literal would remain unredacted in both the
raw line content and any output derived from it. **Finding: subtle-bug /
residual security-issue — incomplete redaction on multi-occurrence lines.**

## Step 4 — Outcome

This finding was real, not hypothetical — it was fixed immediately in the
same session (`pattern.regex.sub()` instead of `search()`+slice, redacting
*all* occurrences), with a regression test added
(`tests/test_risk_scanner.py::test_all_occurrences_of_a_secret_pattern_on_one_line_are_redacted`).
`dogfood.diff` above captures the state *before* this second fix — i.e. it
still contains the multi-occurrence gap — so a re-run of this same review
against the *current* `risk_scanner.py` would no longer surface it. Logged as
L6 in `project-memory-bank/12-known-limitations.md` (status: fixed).

## Why this matters as evidence

The deterministic risk-flag layer produced zero leads for this diff — it was
silent by design, since no pattern was mechanically present. The actual
defect was only reachable by the agent reasoning about the code's *semantics*
(search vs. sub, first-match vs. all-matches), which is precisely the
division of labor Phase 2's architecture decision (`ADR-007`) is built on: the
engine catches what's mechanical, the agent catches what requires judgment.
