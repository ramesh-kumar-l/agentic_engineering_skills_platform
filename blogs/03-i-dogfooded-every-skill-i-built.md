# I Dogfooded Every Skill I Built — and Found a Real Bug Every Single Time

*Part 3 of 5 in the Agentic Engineering Skills Platform series. Every bug
described here is real, documented in
[`project-memory-bank/12-known-limitations.md`](../project-memory-bank/12-known-limitations.md),
and fixed with a regression test that's still in the suite.
[Repo README](../README.md) · [Part 2](02-two-architectures-for-ai-agent-skills.md).*

## The pattern that kept repeating

Five skills built across five phases. Every single one shipped with a full
test suite and an 8-fixture evaluation harness before it ever touched real
work. And every single one still had a real, user-facing bug that only
showed up once it was pointed at something genuine — this repo's own
source code, a real diff, a real requirement, a real pending decision. Not
one of the five got a clean pass on real material on the first try.

That's not a story about sloppy engineering. It's a story about what
synthetic fixtures structurally cannot catch, and why "dogfood everything
for real" ended up being one of the highest-leverage habits in this
project — formalized enough that it's now an explicit step in every phase's
plan, not an afterthought.

## L1 — the entry point that was just a comment

The first skill, `codebase-intelligence`, detects CLI entry points by
looking for `if __name__ == "__main__":`. The first implementation did this
with a plain substring search over the whole file's text. It worked
perfectly on every synthetic fixture, because nobody writing a fixture
thinks to put that exact string inside a *docstring*.

Then the skill was pointed at its own repository — the most obvious
dogfood target there is — and five files got misreported as entry points,
including `engine/models.py` and two test files, because they happened to
*mention* `__name__ == "__main__"` in a comment or docstring while
explaining what another file did.

```python
# Before: substring search, matches text anywhere in the file
has_main_guard = '__name__ == "__main__"' in file_text

# After: an actual AST check for a top-level `if` comparing __name__
def _has_main_guard(tree: ast.Module) -> bool:
    for node in tree.body:
        if isinstance(node, ast.If) and _is_name_main_comparison(node.test):
            return True
    return False
```

The fix is small. The point isn't the fix — it's that a 4-fixture synthetic
evaluation harness, deliberately covering entry points, boundary cases, and
edge cases, still didn't include "the phrase appears in a comment," because
whoever writes synthetic fixtures tends to write fixtures that describe the
bug they already know to look for. Real code doesn't cooperate that way.

## L5 and L6 — the secret that leaked twice, from the same fix

`adversarial-diff-reviewer` needs to flag a hardcoded secret added in a
diff without echoing the actual secret value into its own report — a report
that might itself get logged, pasted into a PR comment, or displayed
somewhere. The first implementation redacted the secret in the `RiskFlag`
object it built, but the diff's raw line content — also serialized into the
same JSON/Markdown report — still held the literal, unredacted secret. An
integration test written specifically to check this
(`test_secret_value_never_leaks_into_json_or_markdown`) failed immediately,
before the skill ever shipped — exactly what that test was there for.

The fix mutated the line content in place too. Then, applying the skill's
own adversarial-review workflow to its own diff while building the dogfood
example, a second, subtler gap turned up in *that same fix*:

```python
# risk_scanner.py — the second bug, in the first fix
if pattern.redact:
    matched_text = _REDACTED_PLACEHOLDER
    line.content = pattern.regex.sub(_REDACTED_PLACEHOLDER, line.content)
```

That `sub()` call is actually the *fixed* version. The bug was in an
intermediate version that used `search()` plus string slicing — which finds
and redacts only the *first* match on a line. A line like
`api_key = "AAA"; token = "BBB"` — two secrets, same pattern shape, one
line — would redact the first and silently leak the second. `sub()`
replaces every occurrence in one pass; `search()` plus slicing structurally
cannot.

This is the one entry in the whole limitations log that's a bug found
inside a bug fix — L6 exists specifically because L5's fix didn't get
dogfooded hard enough the first time, and did the second. The regression
test that now guards it,
`test_all_occurrences_of_a_secret_pattern_on_one_line_are_redacted`, exists
because of exactly that near-miss.

## L10 and L13 — a skill's dogfood run finding a *different* skill's gap

Something more interesting started happening from Phase 3 onward:
dogfooding a new skill against real work started surfacing bugs in
*previous* skills.

`acceptance-test-engineer` (Phase 3) was dogfooded against a real,
already-shipped requirement: "define acceptance criteria for
`adversarial-diff-reviewer`'s CLI." Deriving those criteria meant actually
looking at that CLI's real behavior — and its real behavior turned out to
include zero test coverage for `main()` itself: stdin reading, `--out`
directory writing, the nonexistent-path exit path. Nineteen tests existed
for that skill, all against engine internals, none against the CLI wrapper
that's the actual thing a user runs. `feature-planner` (Phase 4) repeated
the exact same discovery shape one phase later, against
`acceptance-test-engineer`'s own CLI — found not by deliberately auditing
test coverage, but as a side effect of grounding "affected files" in a real
module list during a real planning task.

Neither of these gaps was found by looking for them. They were found
because the *task itself was real* — a real requirement, a real planning
target — and a real task's inputs don't stay conveniently contained within
the one skill you're currently testing.

## L16 — the bug found in the very skill doing the dogfooding

The most recent one is the most interesting, because for the first time,
the dogfood run caught a bug in the *same skill being dogfooded*, not a
different one.

`security-context-guard`'s action classifier needs to recognize phrases
like "push this to origin" as a `Publishing`-category high-risk action. The
first version matched a verb and its object within a fixed character-distance
window:

```python
# The original approach (not the final code) — a fixed-distance window
re.compile(r"(?i)\bpush\b.{0,20}\b(origin|main|shared|remote|repository|repo)\b")
```

Twenty characters is enough for "push to origin" or "push to the remote."
It is not enough for real phrasing. The actual sentence this skill was
dogfooded against — a genuine, in-session pending decision about whether to
commit and push this very phase's own files — read:

> "Commit and push the new Security Context Guard skill files
> (skills/security-context-guard/, evaluations/security-context-guard/,
> project-memory-bank updates) to the shared origin repository."

That's 150+ characters between "push" and "origin," almost entirely taken
up by a parenthetical list of the exact files being pushed. The first run
of the CLI against this real sentence produced `suggested_verdict=AUTHORIZE`
with zero action-category matches — a false negative on precisely the kind
of decision this skill exists to catch, on the first real thing it was ever
pointed at.

The instinct at that point is to widen the window — 20 to 80, say. That was
tried, and it still wasn't enough, because there's no principled way to
pick a "big enough" fixed distance for free-text phrasing in general; any
number is just a slightly less wrong magic constant. The actual fix
abandoned distance windows entirely:

```python
_SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")

@dataclass(frozen=True)
class ActionPattern:
    pattern_id: str
    category: str
    description: str
    regex: re.Pattern[str] | None = None
    verb_regex: re.Pattern[str] | None = None
    object_regex: re.Pattern[str] | None = None

    def matches(self, text: str) -> re.Match[str] | None:
        if self.regex is not None:
            return self.regex.search(text)
        for sentence in _SENTENCE_SPLIT.split(text):
            verb_match = self.verb_regex.search(sentence)
            object_match = self.object_regex.search(sentence)
            if verb_match and object_match:
                return verb_match
        return None
```

Same-sentence co-occurrence, not proximity. It doesn't matter how far apart
"push" and "origin" are, as long as they're in the same sentence — which
matches how the actual ambiguity in real phrasing works, rather than
guessing at a number. The regression test that pins this down uses the
exact real sentence that exposed the gap, paired with a negative test
confirming the fix doesn't overcorrect into matching "push" and "origin"
anywhere in the whole text regardless of sentence boundaries.

## The tally, and the actual lesson

| ID | Skill | Found by dogfooding against | Fixed same-session? |
|---|---|---|---|
| L1 | codebase-intelligence | This repo's own source | Yes |
| L5 | adversarial-diff-reviewer | A real in-session diff | Yes |
| L6 | adversarial-diff-reviewer | The skill's own review of its own diff | Yes |
| L10 | adversarial-diff-reviewer *(found by acceptance-test-engineer)* | A real, already-shipped requirement | Yes |
| L13 | acceptance-test-engineer *(found by feature-planner)* | A real planning task against this repo | Yes |
| L16 | security-context-guard | A real pending git-push decision | Yes |

Six findings, five skills, five separate phases, one recurring shape: every
one of these gaps survived a full test suite and a full synthetic
evaluation harness, and every one of them fell within one real run. This
isn't an argument against synthetic fixtures — they're still what catches
regressions and what makes the evaluation harnesses possible at all. It's
an argument that synthetic fixtures and real dogfooding are catching
*structurally different classes of bugs*, and skipping the second one means
shipping the whole first category — the one made of the exact assumptions
you didn't know you were making — straight to whoever uses it next.

**Next in this series:** [Your AI Eval Says 100%. That Should Worry You.](04-your-ai-eval-says-100-percent.md)
— why four perfect evaluation scores in a row across four different skills
is the loudest unaddressed problem in this project, not a success story.
