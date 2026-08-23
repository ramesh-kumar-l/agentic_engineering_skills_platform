# Case 07 — unresolved-new-file

- **Input**: `fixtures/case-07-unresolved-new-file/diff.txt` (a brand new
  file, `engine/new_feature.py`, added with one small function) + a synthetic
  `ci_report.json` that predates this file (it is not listed in `modules`).
- **Context**: exercises the "genuinely new file, not yet in the composed
  report" unresolved case — distinct from `refactoring-safety`'s "expected-
  absent rename destination" case, but the same underlying "unresolved does
  not mean unsafe or fake" principle.
- **Expected Behavior**: the file does not resolve (`resolved_module_path`
  is `null`); structural tier defaults to `low` with a warning that no
  changed file resolved against the report; `modified-signature-no-test-
  change` still fires (a new `def` line with no matching test file in the
  diff); `overall_risk_tier == "medium"` per the rule table (low tier + flag
  + no coverage -> medium).
- **Acceptance Criteria**: the actual derivation must NOT read the
  unresolved status as proof of safety, and must flag that structural
  blast radius could not be derived from real data for this specific file.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating an unresolved new file as automatically
  low-risk with no caveat; silently dropping the file from the report instead
  of surfacing it with an explicit warning.
