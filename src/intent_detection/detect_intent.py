"""
Intent Detection Layer

Responsibility:
- Classify user query into one or more predefined intents.
- Return structured output with confidence scores.

Does NOT:
- Route documents
- Refuse requests
- Escalate issues
- Apply governance logic
"""

import os
import json
from typing import Dict, List
from groq import Groq
from dotenv import load_dotenv



# 🔒 Allowed intent labels (single source of truth)
ALLOWED_INTENTS = {
    "access_request",
    "account_closure",
    "refund_query",
    "billing_query",
    "security_policy_query",
    "support_process_query",
}


CONFIDENCE_THRESHOLD = 0.5


class IntentDetector:

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"

    def detect(self, user_text: str) -> Dict[str, List[Dict]]:
        """
        Returns:
        {
            "intents": [
                {"name": str, "confidence": float}
            ]
        }
        """

        system_prompt = f"""
You are an intent classifier.

You MUST choose only from these intent labels:
{list(ALLOWED_INTENTS)}

Return STRICT JSON in this exact format:

{{
  "intents": [
    {{
      "name": string,
      "confidence": float (0 to 1)
    }}
  ]
}}

Rules:
- Multiple intents are allowed.
- If unsure, return empty list.
- Do NOT explain.
- Do NOT add extra fields.
"""

        response = self.client.chat.completions.create(
            model=self.model,
            temperature=0,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
        )

        raw = response.choices[0].message.content.strip()

        try:
            parsed = json.loads(raw)
        except Exception:
            # Fail-safe fallback
            return {"intents": []}

        validated_intents = []

        for intent in parsed.get("intents", []):
            name = intent.get("name")
            confidence = intent.get("confidence", 0)

            # 🔒 Strict validation
            if (
                name in ALLOWED_INTENTS
                and isinstance(confidence, (int, float))
                and confidence >= CONFIDENCE_THRESHOLD
            ):
                validated_intents.append({
                    "name": name,
                    "confidence": float(confidence),
                })

        return {"intents": validated_intents}