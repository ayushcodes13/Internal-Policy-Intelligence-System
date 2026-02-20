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

from typing import Dict, Any

from src.intent_detection.detect_intent import detect_intent
from src.routing.route_intent import route_intent

from src.retrieval.retrieve import retrieve_chunks
from src.rules.constraint_rules import apply_constraint_rules
from src.rules.governance_rules import GovernanceEngine
from src.rules.types import GovernanceVerdict

from src.rules.handlers.escalation_handler import handle_escalation
from src.rules.handlers.refusal_handler import handle_refusal


class RAGPipeline:

    def __init__(self):
        self.governance = GovernanceEngine()

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

        # 7️⃣ SAFE → Generation Placeholder
        return self._generate_answer(user_query, cleaned_chunks)

    def _generate_answer(self, user_query: str, cleaned_chunks):
        """
        Placeholder generation.
        Replace later with proper RAG prompt.
        """

        return {
            "status": "SAFE",
            "message": "Answer generated successfully (placeholder).",
            "context_used": len(cleaned_chunks),
        }