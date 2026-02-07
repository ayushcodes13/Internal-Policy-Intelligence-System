# src/ Directory Structure and Mental Model

## Core Concept (One Sentence)

src/ is a one-way conveyor belt.
Each folder does exactly one job, passes output forward, and never looks back.

If something breaks, you know where and why.

---

## intent_detection/

### detect_intent.py

**Job:**
Given a user question → decide what the question is about.

That's it.

**Input:**
```
"How can I close my account and get a refund?"
```

**Output:**
```
[
  { "intent": "account_closure", "confidence": 0.81 },
  { "intent": "refund_query", "confidence": 0.67 }
]
```

**What it does NOT do:**
- doesn't choose documents
- doesn't apply rules
- doesn't answer anything

**Think of it as:**
"Labeling the question, not solving it."

---

## routing/

### route_intent.py

**Job:**
Take detected intents → decide which document buckets are allowed.

**Input:**
```
[
  { "intent": "account_closure", "confidence": 0.81 }
]
```

**Output:**
```
{
  "allowed_sources": ["policies", "faqs"]
}
```

**Important:**
- It reads rules from ROUTING_MAP.md
- It does NOT care about the question text
- It does NOT know what's inside documents

**Think of it as:**
"Which rooms are unlocked before searching?"

---

## retrieval/ (this is actual RAG)

### chunker.py

**Job:**
Split documents into searchable chunks.

**Why this exists:**
- LLMs can't search whole documents well
- Small chunks improve relevance
- Metadata sticks to each chunk

**Example:**
```
account_closure_policy.md
→ 12 chunks
→ each chunk has:
   - text
   - source_type
   - owner
   - last_updated
```

### embedder.py

**Job:**
Turn text chunks into vectors.

Input: text
Output: numbers

No business logic. No intelligence.

It's a translator.

### vector_store.py

**Job:**
Store and search embeddings.

**It answers:**
"Given this question vector, which chunks are closest?"

**It does NOT know:**
- what is correct
- what is allowed
- what should be answered

Just similarity.

### retrieve.py

**Job:**
The bridge between routing and vector search.

**What it does:**
1. Accepts:
   - question
   - allowed_sources (from routing)
2. Queries vector store
3. Filters results by metadata
4. Returns top-k chunks

**This is where:**
- routing actually matters
- metadata becomes powerful

---

## pipeline/

### rag_pipeline.py

**Job:**
Wire everything together in order.

**Rough flow:**
```
question
→ detect_intent
→ route_intent
→ retrieve
→ return chunks (for now)
```

**Later this file will grow:**
- rules
- refusals
- final answer generation

But not yet.

---

## utils/

### loaders.py

**Job:**
Boring but critical glue.

**Handles:**
- reading markdown files
- extracting metadata headers
- loading documents consistently

**Why this matters:**
- keeps ingestion clean
- avoids copy-paste logic
- reduces silent bugs

---

## Why This Structure Is Correct (Key Insight)

Each file answers one question only:

| File | Question it answers |
|------|---------------------|
| detect_intent.py | What is being asked? |
| route_intent.py | What may be searched? |
| chunker.py | How is text split? |
| embedder.py | How is text represented? |
| vector_store.py | What is similar? |
| retrieve.py | What is relevant and allowed? |
| rag_pipeline.py | How does it all flow? |

If a bug appears, you don't panic.
You know which question was answered wrongly.

---

## Final Reality Check

**If someone says:**
"Why not just one file?"

**The answer is:**
"Because systems fail at boundaries, not functions."

You're building boundaries.

---

## Next Step

Next step should be hands-on, otherwise this stays abstract.

Say:
"Let's implement chunker + loader first."

That's the safest place to start coding without breaking your mental model.