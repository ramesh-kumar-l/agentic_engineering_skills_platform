# Case 06 — hotspot-module-mentioned

- **Input**: `fixtures/case-06-hotspot-module-mentioned/narrative.txt` — a
  decision naming "the scanner module"; the composed CI report marks
  `engine/scanner.py` as a real hotspot (fan_in=9).
- **Context**: tests location_resolver's word-boundary resolution
  succeeding and priority_scorer escalating to HIGH on real structural
  grounding — the intended positive path for this skill's whole reason to
  compose on codebase-intelligence.
- **Expected Behavior**: one candidate, `resolved_module_path ==
  "engine/scanner.py"`, `suggested_capture_priority == "HIGH"`.
- **Acceptance Criteria**: resolution succeeds; priority is HIGH, grounded
  in real fan_in/hotspot data, not just narrative wording.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: this is also the resolver's positive-match
  regression test — confirms the word-boundary fix doesn't also reject
  legitimate matches (only the L23-style embedded-substring false positive).
