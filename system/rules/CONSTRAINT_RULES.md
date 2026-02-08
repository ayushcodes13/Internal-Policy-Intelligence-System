# Constraint Rules

## Purpose
Constraint rules enforce hard boundaries on what content
is allowed to be used for answering.

These rules run first.

## When This Runs
Immediately after retrieval.

## Inputs
- Retrieved chunks
- Chunk metadata

## Decisions This Can Make
- DROP_CHUNK
- BLOCK_RESPONSE
- ALLOW_CONTINUE

## Rules
- Chunks from `notes/` are always dropped
- Chunks missing required metadata are dropped
- If no valid chunks remain → INSUFFICIENT_CONTEXT
- If conflicting authoritative sources exist → BLOCK_RESPONSE
- Policies override FAQs and SOPs
- Outdated-only context requires disclaimer or block

## Out of Scope
- Escalation decisions
- Safety refusals
- Answer generation