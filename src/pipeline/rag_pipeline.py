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

from src.utils.logger import StructuredLogger
import time


class RAGPipeline:

    def __init__(self):
        self.logger = StructuredLogger(enable_file_logging=True)
        
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

        start_time = time.time()

        # 1️⃣ Intent Detection
        intent_result = self.intent_detector.detect(user_query)

        # 2️⃣ Routing
        routing_result = route_intent(intent_result["intents"])
        allowed_owners = routing_result.get("allowed_owners", [])

        # 3️⃣ Retrieval
        retrieval_start = time.time()
        retrieval_output = retrieve_chunks(
            user_query=user_query,
            allowed_owners=allowed_owners,
            debug=False
        )

        if isinstance(retrieval_output, dict):
            retrieved_chunks = retrieval_output["final_chunks"]
            diagnostics = retrieval_output["diagnostics"]
        else:
            retrieved_chunks = retrieval_output
            diagnostics = []   
            
        retrieval_time_ms = round((time.time() - retrieval_start) * 1000, 2)
        
        for d in diagnostics:
            print("\n=== RETRIEVAL DIAGNOSTICS ===")
            print(
                f"Path: {d['path']} | "
                f"Owner: {d['owner']} | "
                f"is_latest: {d['is_latest']} | "
                f"Score: {round(d['score'], 4)} | "
                f"Filtered: {d['filtered_out']} | "
                f"Reason: {d['reason']}"
            )
        print("================================\n")

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
        result = handle_verdict(
            verdict=verdict,
            user_query=user_query,
            cleaned_chunks=cleaned_chunks,
            pipeline=self
        )
        result["verdict"] = verdict.name

        total_time_ms = round((time.time() - start_time) * 1000, 2)

        # 7️⃣ Structured Log
        self.logger.log(
            event="QUERY_EXECUTION",
            data={
                "query": user_query,
                "intents": intent_result.get("intents"),
                "allowed_owners": allowed_owners,
                "retrieval_time_ms": retrieval_time_ms,
                "retrieved_count": len(retrieved_chunks),
                "governance_verdict": verdict.name,
                "final_status": result.get("status"),
                "confidence": result.get("confidence"),
                "total_latency_ms": total_time_ms,
            }
        )

        return result


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
    
    

## python -m src.pipeline.rag_pipeline -> to run the pipeline locally 