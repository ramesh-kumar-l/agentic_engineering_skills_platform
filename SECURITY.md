# Security Policy

## Reporting a vulnerability

If you find a security issue in this project (a skill, evaluation harness, or
any tooling here), please report it privately rather than opening a public
issue. Open a private security advisory via this repository's GitHub Security
tab, or contact the maintainer directly through GitHub.

Please include: affected file/skill, reproduction steps, and potential impact.
We'll acknowledge reports and aim to respond with a remediation plan before any
public disclosure.

## Scope

This project's security model — least privilege, least context, explicit
permissions, data minimization, human approval, and auditability — is
documented in
[`project-memory-bank/06-security-model.md`](project-memory-bank/06-security-model.md).
That document governs how skills are expected to handle tool access, context,
and high-risk actions; treat deviations from it as security-relevant.

## Current state

Phase 0 — no skills or executable code exist yet, so there is no runtime attack
surface today. This policy exists ahead of that so reporting channels are in
place before publication.
