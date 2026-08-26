# case-06-top-n-limits-output

**Category**: top-n

Five records all genuinely match the task; `--top-n 2` truncates the
result to the top two by score. Confirms truncation happens at the report
layer after full scoring, not by skipping candidates early.
