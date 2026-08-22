# Security Context Guard — Real Dogfood Run + Pilot C (A7)

This is a real run against this platform's own repository, in this same
session, targeting a real pending decision — not a synthetic fixture. It
also serves as **Pilot C**, the first (N=1, self-run, explicitly-labeled,
ADR-009-governed) internal pilot toward
[[16-assumptions-and-validation]] A7: "does security handling materially
increase trust?"

## Step 1 — The real content and the real decision

Phase 5's new files (`skills/security-context-guard/`,
`evaluations/security-context-guard/`) are untracked, uncommitted, and not
yet pushed. This session will need to ask before committing/pushing them —
a real `Publishing`/shared-state action per
[[06-security-model]]. That is exactly the kind of decision this skill
exists to support, so it was run against it for real:

```
python -m engine.cli engine/scanner.py \
  --action "Commit and push the new Security Context Guard skill files \
  (skills/security-context-guard/, evaluations/security-context-guard/, \
  project-memory-bank updates) to the shared origin repository." \
  --paths engine/scanner.py engine/classification.py engine/secret_patterns.py \
  --format both --out ../../examples/security-context-guard/output
```

`engine/scanner.py` is real, already-written source from this same phase —
not a synthetic sample.

## Step 2 — First run found a real bug (L16, fixed same-session)

The first run of the command above produced `suggested_verdict = AUTHORIZE`
with **zero** action-category matches — the `publishing` pattern's
verb+object proximity window (`push ... .{0,20} ... origin`) was tuned
against short synthetic phrasing and completely missed this real sentence,
where "push" and "shared origin repository" are separated by a 150+
character parenthetical file list. Widening the window to 80 characters
(the first attempted fix) still wasn't enough — the actual distance was 150+
characters, and no fixed window is well-justified for free-text phrasing.

**Real fix**: replaced the fixed-distance-window approach with **same-
sentence co-occurrence** — `ActionPattern.matches()` splits the action text
into sentences and checks whether the verb pattern and the object pattern
each appear somewhere in the *same* sentence, regardless of distance. This
is a better-justified design (matches how the ambiguity in real phrasing
actually works), not just a bigger magic number. Regression test:
`tests/test_action_patterns.py::test_publishing_matches_with_an_object_list_
between_verb_and_target`, plus a paired negative test
(`test_publishing_does_not_match_push_in_an_unrelated_later_sentence`)
confirming the same-sentence constraint doesn't just degrade into "matches
anywhere in the whole text." Logged as **L16** in
[[12-known-limitations]] — the third cross-phase pattern of "a real
dogfood run on real phrasing found a gap a synthetic fixture didn't," after
L1 (Phase 1) and L13 (Phase 4), but this time the gap was in the same
skill being dogfooded, not a different one.

## Step 3 — Re-run after the fix

```
$ python -m engine.cli engine/scanner.py --action "Commit and push ..." \
    --paths engine/scanner.py engine/classification.py engine/secret_patterns.py \
    --format both --out ../../examples/security-context-guard/output

Sensitivity: low
Suggested verdict: REQUIRES_HUMAN_APPROVAL
Evidence: 1 high-risk action category match(es): Publishing.
Action flags: [Publishing] `publishing-push` — Mentions pushing to a
shared remote destination.
```

No secrets or PII in the real source content (correct — it's clean, already
-committed-quality code); the action is correctly classified as `Publishing`
and recommends human approval before the push happens. See
`output/security-guard-report.md` for the full report.

## Step 4 — Pilot C: structured report vs. an unstructured judgment call

**Unstructured baseline** (what this session would say without the skill,
written before re-reading the structured output above): *"These are new,
clean files — nothing in the diff looks sensitive. I'd still ask before
pushing, since pushing to the shared repo is something I always confirm
first regardless of content."*

**Structured report**: `REQUIRES_HUMAN_APPROVAL`, sensitivity `low`, 0
secret/PII matches, 1 action-category match (`Publishing`), stated evidence
trail.

**Honest comparison**: for this specific, low-complexity case, the two
conclusions match — this session's existing bounded-autonomy behavior
already treats a git push as needing confirmation, independent of this
skill. So on *this* case, the structured report did not change the bottom-
line decision a human would see. What it *did* add: (1) an explicit,
auditable evidence trail (word count, exact zero-match counts per category,
the specific matched pattern name) that an unstructured pass would not
spontaneously produce with this level of structure — useful for the
`audit-entry` checklist category regardless of whether the verdict itself
was surprising; (2) the dogfood process itself caught a real false-negative
(Step 2) before it could ever mislead a real decision, which an unstructured
judgment call has no equivalent safeguard for.

**Conclusion, scoped honestly**: this is one data point, self-rated, not
real user feedback — it does **not** validate A7 ("security handling
materially increases trust"), and A7's status stays `UNKNOWN`. It shows the
workflow is executable, produces a real evidence trail, and — via the L16
finding — that dogfooding on real phrasing has concrete value even for a
skill whose job is safety, not just planning. The real validation experiment
A7 calls for (qualitative feedback from an actual user deciding whether to
grant more permissions) still requires someone other than this session's
agent.
