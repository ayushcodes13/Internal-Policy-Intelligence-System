"""
Governance Layer

Question:
“What should the system do with this query?”

This layer:
- Uses an LLM to detect high-level risk signals
- Classifies the query into structured governance signals
- Applies deterministic priority rules
- Returns a final GovernanceVerdict enum

It does NOT:
- Escalate
- Refuse directly
- Generate answers
- Modify retrieved documents

It only decides the verdict.

Signal Detection → Deterministic Resolution → Verdict

This keeps decision logic separate from action logic.
"""

import os
import json
from typing import List, Dict
from groq import Groq # Keep Groq import
from src.rules.types import GovernanceVerdict


class GovernanceEngine:
    """
    Governance Layer

    Responsibilities:
    - Use LLM to detect risk signals
    - Apply deterministic priority rules
    - Return a final GovernanceVerdict

    It does NOT:
    - escalate
    - refuse
    - generate answers
    - modify chunks
    """

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    # --------------------------------------------------------
    # Public method
    # --------------------------------------------------------

    def evaluate(
        self,
        user_query: str,
        cleaned_chunks: List[Dict],
    ) -> GovernanceVerdict:
        """
        Main governance evaluation entrypoint.
        """

        signals = self._llm_classify(user_query)
        verdict = self._resolve(signals)

        # Deterministic domain enforcement:
        # If LLM says SAFE but nothing was retrieved,
        # this is out-of-domain → refuse.
        if verdict == GovernanceVerdict.SAFE and not cleaned_chunks:
            return GovernanceVerdict.REFUSE_INVALID

        return verdict

    # --------------------------------------------------------
    # LLM Classification
    # --------------------------------------------------------

    def _llm_classify(self, user_query: str) -> Dict:
        """
        Calls LLM to detect:
        - invalid input
        - escalation needed
        - policy denial
        """

        system_prompt = """
You are a governance classifier.

You must return STRICT JSON with this exact structure:

{
  "is_invalid": boolean,
  "is_escalation": boolean,
  "is_policy_denial": boolean
}

Rules:

- is_invalid = true if query is nonsense, malicious, or unrelated to system domain.
- is_escalation = true if if the user is reporting an active security issue, legal threat, account compromise, fraud, legal risk, security breach, unusual financial claim, or anything that must be reviewed by a human. Do NOT mark escalation for informational queries discussing policies, processes, or procedures.
- is_policy_denial = true if the user is requesting something that is explicitly not allowed by policy.

Do NOT explain.
Do NOT add extra fields.
Return JSON only.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query},
            ],
        )

        raw = response.choices[0].message.content.strip()

        try:
            return json.loads(raw)
        except Exception:
            # If parsing fails → safest fallback
            return {
                "is_invalid": False,
                "is_escalation": False,
                "is_policy_denial": False,
            }

    # --------------------------------------------------------
    # Deterministic Resolver
    # --------------------------------------------------------

    def _resolve(self, signals: Dict) -> GovernanceVerdict:
        
        if signals.get("is_invalid"):
            return GovernanceVerdict.REFUSE_INVALID
        
        if signals.get("is_policy_denial"):
            return GovernanceVerdict.REFUSE_POLICY
        
        if signals.get("is_escalation") and signals.get("confidence") == "low":
            return GovernanceVerdict.SAFE
        
        if signals.get("is_escalation"):
            return GovernanceVerdict.ESCALATE
        
        return GovernanceVerdict.SAFE