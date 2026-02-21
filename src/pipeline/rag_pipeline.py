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

from src.intent_detection.detect_intent import detect_intent
from src.routing.route_intent import route_intent

from src.retrieval.retrieve import retrieve_chunks
from src.rules.constraint_rules import apply_constraints as apply_constraint_rules
from src.rules.governance_rules import GovernanceEngine
from src.rules.types import GovernanceVerdict

from src.rules.handlers.escalation_handler import handle_escalation
from src.rules.handlers.refusal_handler import handle_refusal


class RAGPipeline:

    def __init__(self):
        self.governance = GovernanceEngine()

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def run(self, user_query: str) -> Dict[str, Any]:

        # 1️⃣ Intent Detection
        intent_result = detect_intent(user_query)

        # 2️⃣ Routing
        routing_result = route_intent(intent_result)
        allowed_owners = routing_result.get("allowed_owners", [])
        allowed_source_types = routing_result.get("allowed_source_types")

        # 3️⃣ Retrieval
        retrieved_chunks = retrieve_chunks(
            user_query=user_query,
            allowed_owners=allowed_owners,
        )

        # 4️⃣ Constraint Rules
        cleaned_chunks = apply_constraint_rules(
            chunks=retrieved_chunks,
            allowed_owners=allowed_owners,
            allowed_source_types=allowed_source_types,
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
        Real RAG generation using Groq.
        Strictly grounded in retrieved context.
        """

        if not cleaned_chunks:
            return {
                "status": "SAFE",
                "answer": "The requested information is not available in the current policy documents.",
                "context_used": 0,
            }

        # Use top 5 chunks only to control token usage
        top_chunks = cleaned_chunks[:5]

        context_text = "\n\n".join(
            chunk.get("content", "") for chunk in top_chunks
        )

        system_prompt = """
You are a strict internal support assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not clearly supported by the context, respond exactly with:
  "The requested information is not available in the current policy documents."
- Do NOT invent policies.
- Do NOT speculate.
- Be concise and factual.
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

        return {
            "status": "SAFE",
            "answer": response.choices[0].message.content.strip(),
            "context_used": len(top_chunks),
        }
        
        
        
## for local testing
if __name__ == "__main__":
		pipeline = RAGPipeline()
		test_query = "What is the company's policy on remote work?"
		result = pipeline.run(test_query)
		print(result)
