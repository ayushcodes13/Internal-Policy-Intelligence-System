# Refusal Rules

## Purpose

Refusal rules define when the system must not provide a normal answer.

Refusal is different from escalation.

Refusal ends the interaction with a controlled response.

---

## Core Question

“Is this request invalid or prohibited under policy?”

---

## Refusal Types

### 1. REFUSE_INVALID

The query is outside supported domain.

Examples:
- unrelated personal requests
- creative writing
- coding help unrelated to internal policies
- nonsensical input

Response characteristics:
- short
- neutral
- domain-scoped clarification

---

### 2. REFUSE_POLICY

The query is valid and within domain,
but the requested outcome violates policy.

Example:
User requests a refund after termination due to policy violation.

Response characteristics:
- explain relevant policy
- clearly state restriction
- remain neutral and factual
- do not imply personal judgment

This is structured denial, not silence.

---

## What Refusal Is NOT

Refusal does NOT:
- clean documents
- escalate cases
- interpret policy hierarchy

Refusal is a final response action.

---

## Output

One of:
- REFUSE_INVALID
- REFUSE_POLICY