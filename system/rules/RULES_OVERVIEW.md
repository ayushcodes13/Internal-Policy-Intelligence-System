# Rules System Overview

## Purpose
The rules layer evaluates retrieved content and decides whether the system
is allowed to respond, must escalate, or must refuse.

Rules do not retrieve documents.
Rules do not generate answers.

They only judge.

## When This Runs
Rules execute **after retrieval** and **before generation**.

## Inputs
- Retrieved document chunks
- Chunk metadata
- Detected intents
- Routing scope

## Decisions This Layer Can Make
- ALLOW
- ALLOW_WITH_DISCLAIMER
- ESCALATE
- REFUSE
- INSUFFICIENT_CONTEXT

## Rule Categories
- Constraint rules: hard boundaries
- Escalation rules: human handoff
- Refusal rules: absolute denial

## Out of Scope
- Intent detection
- Routing
- Similarity scoring
- Answer phrasing