# Constraint Rules

## Purpose

Constraint rules clean the retrieved context.

They operate immediately after retrieval and before governance.

This layer is about **documents**, not users and not decisions.

---

## Core Question

“Given what was retrieved, which chunks are allowed to remain in context?”

---

## Scope

Constraint rules:

- remove internal-only documents (notes, drafts, memos)
- enforce owner boundaries
- enforce allowed source types
- resolve version dominance (newer version replaces older)
- remove duplicate or redundant chunks

Constraint rules do NOT:

- escalate cases
- refuse user requests
- interpret policy meaning
- decide whether the user is allowed something
- generate explanations

They only clean the context.

---

## Inputs

- retrieved_chunks (List[Dict])
- metadata fields (owner, source_type, last_updated, path)

---

## Outputs

- cleaned_chunks (List[Dict])

This layer never stops the pipeline.

It never returns a verdict.

It only returns a filtered list of chunks.

---

## Version Dominance Rule

If multiple versions of the same policy exist:

- Keep the most recent version.
- Remove outdated versions.

Version comparison is based on:
- `last_updated`
- explicit version tags (e.g., v2 > v1)

---

## Internal Document Removal

The following must always be removed:

- source_type: notes
- drafts
- internal memos
- experimental documents

Even if retrieval returns them.

---

## Design Principle

Constraint rules protect the system from bad context.

They ensure that only authoritative, allowed documents move forward.

They do not judge the user.
They do not judge the request.

They clean the environment for governance.