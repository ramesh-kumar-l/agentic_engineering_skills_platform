# case-07-missing-ci-report

**Category**: precondition-failure

No `ci_report.json` exists in the fixture directory. Exercises ADR-010's
required-composition hard failure (reused an eleventh time) — the engine
must refuse to retrieve anything rather than silently proceeding with
module resolution disabled.
