# ROUTING.md

## Purpose

Routing decides **which document buckets are eligible for retrieval** after intent detection.

Routing does NOT:
- classify user intent
- interpret user meaning
- apply business rules or conflict resolution
- generate answers

Routing ONLY maps:
**intent → allowed document groups**

This separation is intentional to keep the system simple, auditable, and low-error.

---

## Inputs

Routing receives:
- One or more detected intents
- Each intent has a confidence score
- Intents are produced by semantic intent detection (LLM-based)

Example input:
- intent: `account_closure`
- confidence: `0.82`

---

## Outputs

Routing produces:
- A list of document categories allowed for retrieval
- No ranking, no filtering inside documents

Example output:
- allowed_sources:
  - policies
  - faqs
  - sops

---

## Routing Principles

1. **Allow-list only**
   - Documents are included explicitly
   - Anything not listed is excluded by default

2. **No conditional logic**
   - Routing does not inspect question wording
   - Routing does not reason about consequences
   - Routing does not infer edge cases

3. **No cross-intent leakage**
   - Each intent has its own routing definition
   - Overlap is explicit, never assumed

4. **Internal notes are never routed**
   - `notes/` is excluded from all routing outputs
   - Notes exist for human context and future rules only

---

## Routing Table

### Intent: access_request

Allowed document sources:
- policies
- sops
- faqs

Excluded:
- notes

---

### Intent: account_closure

Allowed document sources:
- policies
- faqs

Excluded:
- sops
- notes

---

### Intent: refund_query

Allowed document sources:
- policies
- sops
- faqs

Excluded:
- notes

---

### Intent: billing_query

Allowed document sources:
- policies
- faqs

Excluded:
- sops
- notes

---

### Intent: security_policy_query

Allowed document sources:
- policies
- faqs

Excluded:
- sops
- notes

---

### Intent: support_process_query

Allowed document sources:
- sops
- faqs

Excluded:
- policies
- notes

---

## Multiple Intents Handling

If multiple intents are detected:
- Union of allowed document sources is used
- Exclusions always win over inclusion for `notes`

Example:
- intents: `refund_query`, `billing_query`
- allowed_sources:
  - policies
  - sops
  - faqs

---

## What Routing Does NOT Handle

The following are explicitly out of scope:
- conflicting documents
- outdated policies
- compliance enforcement
- escalation logic
- refusal logic
- hallucination control

These belong to:
- rules layer
- response governance
- traceability layer

---

## Design Rationale

Routing is intentionally boring.

Boring systems:
- fail less
- scale better
- are easier to debug
- survive team changes

All intelligence lives either:
- **before routing** (intent detection)
- **after retrieval** (rules + response)

Routing is the stable bridge in between.