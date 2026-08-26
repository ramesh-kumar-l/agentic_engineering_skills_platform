# Case 01 — two-options-clean

Per-case structure follows `project-memory-bank/05-evaluation-framework.md`.

- **Input**: `fixtures/case-01-two-options-clean/decision.txt` (two explicit
  `Option A:`/`Option B:` markers, stated tradeoffs, reversibility, and a
  security note) + a synthetic `ci_report.json` with 3 modules.
- **Context**: caching (Redis) vs. indexing (Postgres) for a pricing lookup.
- **Expected Behavior**: no decision flags fire (the text is well-specified);
  both options are parsed; blast-radius scoring reveals a real limitation —
  every module path shares the `engine/` prefix, and `engine` itself is
  extracted as a keyword, so both options' blast radius inflates to include
  an unrelated module (`engine/checkout.py`).
- **Acceptance Criteria**: `flags == []`; `option_count == 2`; the actual
  derivation explicitly names the path-prefix keyword collision rather than
  trusting the blast-radius number at face value.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: treating an inflated blast-radius score as real
  evidence; missing the stated tradeoffs/reversibility already in the text.
