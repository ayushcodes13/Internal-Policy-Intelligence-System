"""
Role in simple language: “Record what happened for every query.”

Example log entry:
{
    "query": "Can I get refund after termination?",
    "intents": ["refund_query"],
    "allowed_owners": ["finance"],
    "retrieval_time_ms": 18,
    "governance_verdict": "REFUSE_POLICY",
    "final_status": "REFUSED",
    "confidence": "high",
    "sources": ["billing_and_refund_policy_v2.md"],
    "total_latency_ms": 210
}

This is system telemetry.

If a founder asks:
“Why did it refuse that?”

You can trace it.
Logging is black-box recording.

Structured Logger

Purpose:
- Log structured system events
- Support console + optional file logging
- Keep logs JSON serializable
"""

import json
import os
import time
from typing import Dict, Any

LOG_FILE_PATH = "logs/system_logs.jsonl"

class StructuredLogger:

    def __init__(self, enable_file_logging: bool = True):
        self.enable_file_logging = enable_file_logging

        if enable_file_logging:
            os.makedirs("logs", exist_ok=True)

    def log(self, event: str, data: Dict[str, Any]) -> None:
        """
        Logs a structured event.

        Args:
            event: name of event (e.g., "QUERY_EXECUTION")
            data: dictionary payload
        """

        log_entry = {
            "timestamp": time.time(),
            "event": event,
            "data": data
        }

        # File logging (JSON lines)
        if self.enable_file_logging:
            with open(LOG_FILE_PATH, "a") as f:
                f.write(json.dumps(log_entry) + "\n")