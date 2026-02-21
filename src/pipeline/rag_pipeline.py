"""
RAG Pipeline

Orchestrates the full system:

User Query
→ Intent Detection
→ Routing
→ Retrieval
→ Constraint Rules
→ Governance
→ Handler or Generation

This file contains NO business logic.
It only connects components.
"""

from typing import Dict, Any, List
import os
from groq import Groq
from dotenv import load_dotenv
import json

from src.intent_detection.detect_intent import IntentDetector
from src.routing.route_intent import route_intent

from src.retrieval.retrieve import retrieve_chunks
from src.rules.constraint_rules import apply_constraints as apply_constraint_rules
from src.rules.governance_rules import GovernanceEngine
from src.rules.types import GovernanceVerdict

from src.rules.handlers.escalation_handler import handle_escalation
from src.rules.handlers.refusal_handler import handle_refusal

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

    def run(self, user_query: str) -> Dict[str, Any]:

        # 1️⃣ Intent Detection
        intent_result = self.intent_detector.detect(user_query)
        print("INTENT RESULT:", intent_result)

        # 2️⃣ Routing
        routing_result = route_intent(intent_result["intents"])
        allowed_owners = routing_result.get("allowed_owners", [])
        print("ALLOWED OWNERS:", allowed_owners)
        allowed_source_types = routing_result.get("allowed_source_types")
        print("INTENTS PASSED TO ROUTING:", intent_result["intents"])

        # 3️⃣ Retrieval
        retrieved_chunks = retrieve_chunks(
            user_query=user_query,
            allowed_owners=allowed_owners,
        )

        # 4️⃣ Constraint Rules
        cleaned_chunks = apply_constraint_rules(
    retrieved_chunks,
    allowed_owners
)

        # 5️⃣ Governance
        verdict = self.governance.evaluate(
            user_query=user_query,
            cleaned_chunks=cleaned_chunks,
        )

        # 6️⃣ Action Handling
        if verdict == GovernanceVerdict.ESCALATE:
            return handle_escalation(user_query, cleaned_chunks)

        if verdict in [
            GovernanceVerdict.REFUSE_INVALID,
            GovernanceVerdict.REFUSE_POLICY,
        ]:
            return handle_refusal(verdict)

        # 7️⃣ SAFE → Generation
        return self._generate_answer(user_query, cleaned_chunks)

    def _generate_answer(
        self,
        user_query: str,
        cleaned_chunks: List[Dict],
    ) -> Dict[str, Any]:
        """
        Hardened RAG generation.
        - Structured JSON output
        - Mandatory source citation
        - Mandatory supporting clause extraction
        - Deterministic behavior
        """

        if not cleaned_chunks:
            return {
                "status": "SAFE",
                "answer": None,
                "sources": [],
                "supporting_clauses": [],
                "confidence": "low",
                "context_used": 0,
            }

        # Use top 5 chunks to control token usage
        top_chunks = cleaned_chunks[:5]

        context_blocks = []
        for chunk in top_chunks:
            path = chunk["metadata"].get("path", "unknown")
            text = chunk.get("text", "")
            context_blocks.append(f"Document: {path}\n{text}")

        context_text = "\n\n---\n\n".join(context_blocks)

        system_prompt = """
    You are a strict internal policy assistant.

    You MUST return STRICT JSON in this exact format:

    {
    "answer": string | null,
    "sources": [string],
    "supporting_clauses": [string],
    "confidence": "high" | "medium" | "low"
    }

    Rules:
    - Use ONLY the provided context.
    - If the answer is not clearly supported, set:
        "answer": null,
        "sources": [],
        "supporting_clauses": [],
        "confidence": "low"
    - Every source MUST exactly match a provided document path.
    - Every supporting clause MUST be an exact quote from the context.
    - Do NOT invent policies.
    - Do NOT explain outside JSON.
    - Do NOT add extra fields.
    """

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": f"""User Question:
    {user_query}

    Context:
    {context_text}
    """
                },
            ],
        )

        raw_output = response.choices[0].message.content.strip()

        # 🔐 Safe JSON parsing
        try:
            parsed = json.loads(raw_output)
        except Exception:
            return {
                "status": "SAFE",
                "answer": None,
                "sources": [],
                "supporting_clauses": [],
                "confidence": "low",
                "context_used": len(top_chunks),
            }

        # 🔎 Validate cited sources actually exist in context
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
            "sources": cited_sources,
            "supporting_clauses": parsed.get("supporting_clauses", []),
            "confidence": parsed.get("confidence", "low"),
            "context_used": len(top_chunks),
        }


## for local testing
if __name__ == "__main__":
		pipeline = RAGPipeline()
		test_query = "What is the refund period?"
		result = pipeline.run(test_query)
		print(result)