# Escalation Rules

## Purpose
Escalation rules determine when a question should be
handled by a human instead of the system.

Escalation is not refusal.

## When This Runs
After constraint rules pass.

## Inputs
- Cleaned retrieved chunks
- Detected intents

## Decisions This Can Make
- ESCALATE
- ALLOW_CONTINUE

## Rules
- Requests involving irreversible account actions
- Security incidents or breaches
- Legal or compliance-sensitive topics
- Ambiguous instructions with high impact
- Conflicting user intent signals

## Out of Scope
- Blocking content
- Policy enforcement
- Answer phrasing