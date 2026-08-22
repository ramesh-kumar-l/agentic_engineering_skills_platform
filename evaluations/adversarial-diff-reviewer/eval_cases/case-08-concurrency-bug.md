# Case 08 — concurrency-bug

- **Input**: `fixtures/case-08-concurrency-bug/change.diff`.
- **Context**: `get_or_compute`'s `with lock:` wrapping a check-then-act cache
  pattern is removed.
- **Expected Behavior**: The agent recognizes the removed lock introduces a
  race condition (two threads can both miss the cache and both call
  `compute()`), inferring concurrent use from the prior presence of the lock.
- **Acceptance Criteria**: A reported defect with `category ==
  "concurrency-bug"`, `file == "cache.py"`, mentioning the race condition.
- **Actual Result / Score**: see `../RESULTS.md`.
- **Failure Modes checked**: concurrency bugs are explicitly called out in
  `05-evaluation-framework.md`'s failure-first list as a category regex
  cannot detect — this is the direct test of that category.
