"""
Role in simple language: “Is the system correct across many queries?”

Example test case:

{
    "query": "What is the refund period?",
    "expected_status": "SAFE",
    "expected_source_contains": "billing_and_refund_policy_v2"
}

Evaluation runs 20 such queries and outputs:
	•	Status accuracy: 95%
	•	Retrieval Recall@5: 90%
	•	Refusal precision: 100%

If you ever:
	•	Change retrieval
	•	Add hybrid search
	•	Switch embedding model
	•	Tune governance prompts

Evaluation tells you:
Did it improve or did it break?

THIS IS ONLY USED FOR OFFLINE CASE AND NOT USED IN REALTIME DECISION MAKING.
Evaluation exists for one reason:

To know if your system is actually good — instead of just feeling good about it.
"""

import json
from src.pipeline.rag_pipeline import RAGPipeline


def run():
    pipeline = RAGPipeline()

    with open("evaluation/test_cases.json", "r") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    correct = 0

    print("\n========== EVALUATION START ==========\n")

    for i, case in enumerate(test_cases, 1):
        query = case["query"]
        expected_verdict = case["expected_verdict"]

        result = pipeline.run(query)

        # Directly use exposed internal verdict
        actual_verdict = result.get("verdict", "UNKNOWN")

        passed = actual_verdict == expected_verdict

        if passed:
            correct += 1

        print("================================")
        print(f"Test {i}: {query}")
        print(f"Expected Verdict : {expected_verdict}")
        print(f"Actual Verdict   : {actual_verdict}")
        print(f"Final Status     : {result.get('status')}")
        print(f"Confidence       : {result.get('confidence')}")
        print(f"Result           : {'PASS' if passed else 'FAIL'}")
        print("-" * 50)

    accuracy = (correct / total) * 100

    print("\n========== SUMMARY ==========")
    print(f"Total Tests : {total}")
    print(f"Passed      : {correct}")
    print(f"Failed      : {total - correct}")
    print(f"Accuracy    : {accuracy:.2f}%")
    print("================================\n")


if __name__ == "__main__":
    run()