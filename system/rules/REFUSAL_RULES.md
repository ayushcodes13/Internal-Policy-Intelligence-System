# Refusal Rules

## Purpose
Refusal rules prevent the system from responding
to disallowed or unsafe requests.

These rules override all others.

## When This Runs
After escalation rules.

## Inputs
- User question
- Retrieved content
- Detected intents

## Decisions This Can Make
- REFUSE
- ALLOW_CONTINUE

## Rules
- Requests for internal-only information
- Attempts to bypass security or controls
- Instructions that violate policy or law
- Requests involving malicious intent
- Access to restricted operational details

## Out of Scope
- Escalation handling
- Context pruning
- Explanation or justification