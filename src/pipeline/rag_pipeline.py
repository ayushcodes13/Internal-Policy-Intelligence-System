"""
RAG Pipeline

Orchestrates the full system:

User Query
→ Intent Detection
→ Routing
→ Retrieval
→ Constraint Rules
→ Governance
→ Verdict Handler

This file contains NO decision logic.
It only orchestrates components and handles generation.
"""

from typing import Dict, Any, List
import os
import json
from groq import Groq
from dotenv import load_dotenv

from src.intent_detection.detect_intent import IntentDetector
from src.routing.route_intent import route_intent
from src.retrieval.retrieve import retrieve_chunks
from src.rules.constraint_rules import apply_constraints
from src.rules.governance_rules import GovernanceEngine
from src.rules.handlers.verdict_handler import handle_verdict


class RAGPipeline:

    def __init__(self):
        load_dotenv()

        self.intent_detector = IntentDetector()
        self.governance = GovernanceEngine()

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    # ==========================================================
    # Main Entry
    # ==========================================================

    def run(self, user_query: str) -> Dict[str, Any]:

        # 1️⃣ Intent Detection
        intent_result = self.intent_detector.detect(user_query)

        # 2️⃣ Routing
        routing_result = route_intent(intent_result["intents"])
        allowed_owners = routing_result.get("allowed_owners", [])

        # 3️⃣ Retrieval
        retrieved_chunks = retrieve_chunks(
            user_query=user_query,
            allowed_owners=allowed_owners,
        )

        # 4️⃣ Constraints
        cleaned_chunks = apply_constraints(
            retrieved_chunks,
            allowed_owners
        )

        # 5️⃣ Governance
        verdict = self.governance.evaluate(
            user_query=user_query,
            cleaned_chunks=cleaned_chunks,
        )

        # 6️⃣ Unified Action Handling
        return handle_verdict(
            verdict=verdict,
            user_query=user_query,
            cleaned_chunks=cleaned_chunks,
            pipeline=self
        )

    # ==========================================================
    # SAFE GENERATION
    # ==========================================================

    def _generate_answer(
        self,
        user_query: str,
        cleaned_chunks: List[Dict],
    ) -> Dict[str, Any]:

        if not cleaned_chunks:
            return {
                "status": "SAFE",
                "answer": None,
                "message": None,
                "sources": [],
                "supporting_clauses": [],
                "confidence": "low",
                "context_used": 0,
            }

        top_chunks = cleaned_chunks[:5]

        context_blocks = []
        for chunk in top_chunks:
            path = chunk["metadata"].get("path", "unknown")
            text = chunk.get("text", "")
            context_blocks.append(f"Document: {path}\n{text}")

        context_text = "\n\n---\n\n".join(context_blocks)

        system_prompt = """
You are a strict internal policy assistant.

Return STRICT JSON:

{
  "answer": string | null,
  "sources": [string],
  "supporting_clauses": [string],
  "confidence": "high" | "medium" | "low"
}

Rules:
- Use ONLY provided context.
- Every source must match a document path exactly.
- Supporting clauses must be exact quotes.
- If unsupported, return null answer and low confidence.
- No extra fields.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
User Question:
{user_query}

Context:
{context_text}
"""
                },
            ],
        )

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)
        except Exception:
            return {
                "status": "SAFE",
                "answer": None,
                "message": None,
                "sources": [],
                "supporting_clauses": [],
                "confidence": "low",
                "context_used": len(top_chunks),
            }

        valid_paths = {
            chunk["metadata"].get("path")
            for chunk in top_chunks
        }

        cited_sources = [
            src for src in parsed.get("sources", [])
            if src in valid_paths
        ]

        return {
            "status": "SAFE",
            "answer": parsed.get("answer"),
            "message": None,
            "sources": cited_sources,
            "supporting_clauses": parsed.get("supporting_clauses", []),
            "confidence": parsed.get("confidence", "low"),
            "context_used": len(top_chunks),
        }

    # ==========================================================
    # POLICY DENIAL GENERATION (Evidence-Backed Refusal)
    # ==========================================================

    def _generate_policy_denial(
        self,
        user_query: str,
        cleaned_chunks: List[Dict],
    ) -> Dict[str, Any]:

        if not cleaned_chunks:
            return {
                "status": "REFUSED",
                "answer": None,
                "message": "This request cannot be fulfilled due to existing policy restrictions.",
                "sources": [],
                "supporting_clauses": [],
                "confidence": "low",
                "context_used": 0,
            }

        top_chunks = cleaned_chunks[:5]

        context_blocks = []
        for chunk in top_chunks:
            path = chunk["metadata"].get("path", "unknown")
            text = chunk.get("text", "")
            context_blocks.append(f"Document: {path}\n{text}")

        context_text = "\n\n---\n\n".join(context_blocks)

        system_prompt = """
You are a strict policy enforcement assistant.

Return STRICT JSON:

{
  "message": string,
  "supporting_clauses": [string],
  "confidence": "high" | "medium" | "low"
}

Rules:
- Identify exact clause enforcing denial.
- Quote it exactly.
- Base everything only on context.
- No extra fields.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""
User Question:
{user_query}

Context:
{context_text}
"""
                },
            ],
        )

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)
        except Exception:
            return {
                "status": "REFUSED",
                "answer": None,
                "message": "This request cannot be fulfilled due to existing policy restrictions.",
                "sources": [],
                "supporting_clauses": [],
                "confidence": "low",
                "context_used": len(top_chunks),
            }

        cited_sources = list({
            chunk["metadata"].get("path")
            for chunk in top_chunks
        })

        return {
            "status": "REFUSED",
            "answer": None,
            "message": parsed.get("message"),
            "sources": cited_sources,
            "supporting_clauses": parsed.get("supporting_clauses", []),
            "confidence": parsed.get("confidence", "low"),
            "context_used": len(top_chunks),
        }


# ==========================================================
# Local Test
# ==========================================================

if __name__ == "__main__":
    pipeline = RAGPipeline()
    test_query = "Can I get a refund after account termination due to policy violation?"
    result = pipeline.run(test_query)
    print(result)