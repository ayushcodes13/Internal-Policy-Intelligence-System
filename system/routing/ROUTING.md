# ROUTING.md

## Purpose

Routing determines **which organizational owners are allowed to provide information**
after intent detection.

Routing does NOT:
- detect or classify intent
- understand user questions
- interpret meaning
- apply business rules or policies
- resolve conflicts
- decide correctness
- generate answers

Routing ONLY maps:

**intent → allowed document owners**

This keeps routing stable, auditable, and resistant to document churn.

---

## Input

Routing receives:
- One or more detected intents
- Each intent includes a confidence score

Example:
```yaml
intent: account_closure
confidence: 0.82
```

Routing does not validate confidence.
It assumes intent detection has already done its job.

---

## Output

Routing produces:
- A list of allowed document owners
- Nothing else

Example:
```
allowed_owners:
  - ops
  - support
```

Routing does not rank, filter, or inspect documents.

---

## Core Principles

### 1. Allow-list only

- Only explicitly allowed owners are eligible for retrieval
- All other owners are excluded by default

### 2. Owner-based routing only

- Routing never names folders
- Routing never names files
- Routing never depends on document structure

Owners represent who owns the truth, not how files are organized.

### 3. No conditional logic

- Routing does not inspect question wording
- Routing does not infer edge cases
- Routing does not apply exceptions

### 4. Notes are always excluded

- notes/ are never routed
- Notes exist only for human context and future rule design
- Notes are never surfaced to retrieval

---

## Ownership Model

All documents must declare an owner in metadata:
```
owner: finance | security | ops | support
```

Routing operates only on this field.

---

## Routing Table

### Intent: access_request

**Allowed owners:**
- ops
- security
- support

**Excluded:**
- finance
- notes

---

### Intent: account_closure

**Allowed owners:**
- ops
- support

**Excluded:**
- finance
- security
- notes

---

### Intent: refund_query

**Allowed owners:**
- finance
- support

**Excluded:**
- security
- ops
- notes

---

### Intent: billing_query

**Allowed owners:**
- finance

**Excluded:**
- ops
- security
- support
- notes

---

### Intent: security_policy_query

**Allowed owners:**
- security

**Excluded:**
- finance
- ops
- support
- notes

---

### Intent: support_process_query

**Allowed owners:**
- support
- ops

**Excluded:**
- finance
- security
- notes

---

## Multiple Intents Handling

If multiple intents are detected:
- Allowed owners are merged (set union)
- notes remain excluded in all cases

Example:
```
intents:
  - refund_query
  - billing_query

allowed_owners:
  - finance
  - support
```

Routing does not resolve conflicts between owners.
That responsibility belongs to later layers.

---

## Out of Scope

Routing explicitly does NOT handle:
- conflicting documents
- outdated policies
- compliance enforcement
- escalation logic
- refusal logic
- hallucination control

These belong to:
- rules layer
- governance layer
- traceability layer

---

## Design Rationale

Routing is intentionally boring.

Boring routing:
- breaks less
- survives document growth
- avoids silent bugs
- scales across teams
- remains auditable months later

All intelligence lives:
- before routing → intent detection
- after retrieval → rules and response logic

Routing is the stable bridge in between.

---

## What to do next (no rushing)

1. Update your metadata to ensure every doc has `owner`
2. Adjust `route_intent.py` to output `allowed_owners`
3. Let retrieval filter by owner metadata

No rules yet.
No cleverness yet.
Just clean plumbing.

You're building this the right way.