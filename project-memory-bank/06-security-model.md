# 06 — Security Model

## Principles

```
Least Privilege | Least Context | Explicit Permissions |
Data Minimization | Human Approval | Auditability
```

A prompt is never a complete security boundary.

## Security workflow

```
Classify → Minimize → Sanitize → Authorize → Execute → Audit
```

## Never expose

Credentials, tokens, private keys, passwords, sensitive PII, or confidential data
— unless explicitly authorized through an appropriate secure mechanism.

## Bounded autonomy

Do not optimize for maximum autonomy. Preferred loop:

```
Understand → Plan → Human Approval → Execute → Test → Review →
Human Approval → Complete
```

High-risk actions that always require explicit human approval:

```
Production modifications | Destructive operations | Credentials |
Security controls | Database migrations | Publishing |
External communications
```

## Relationship to trust model

Security classification is one of the required trust-facing fields every skill
must expose (see [[04-skill-contract]]: Trust Status, Evidence, Known Failure
Modes, Security Classification, Provenance). A skill cannot be published
(Section 28 quality gate) without documented security implications.

## Publication quality gate (summary)

A skill may be published only once: purpose, inputs, outputs, usage conditions,
limitations, and security implications are documented; evaluation cases exist;
examples work; no secrets or proprietary information are present; version and
provenance are explicit. Experimental skills must be labeled experimental —
never implied more mature than their evidence.
