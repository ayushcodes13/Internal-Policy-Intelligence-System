from __future__ import annotations

import json
from pathlib import Path

from api.pipeline import run_pipeline
from evaluation.metrics import evaluate_retrieval


ROOT = Path(__file__).resolve().parents[1]
TEST_CASES_PATH = ROOT / "evaluation" / "test_cases.json"


def run() -> None:
    test_cases = json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))

    print("\n========== RETRIEVAL EVALUATION ==========\n")
    retrieval_results = evaluate_retrieval(
        test_cases=test_cases,
        top_k=5,
        deduplicate_documents=True,
    )
    print(f"Total Queries : {retrieval_results['total_queries']}")
    print(f"Recall@5      : {retrieval_results['recall@5']}")
    print(f"MRR           : {retrieval_results['mrr']}")
    print(f"Avg Docs@5    : {retrieval_results['avg_unique_docs_in_top_k']}")

    print("\n========== END-TO-END EVALUATION ==========\n")
    total = len(test_cases)
    correct = 0

    for index, case in enumerate(test_cases, start=1):
        query = case["query"]
        expected_verdict = case["expected_verdict"]
        result = run_pipeline(query)
        actual_verdict = result.get("verdict", "UNKNOWN")
        passed = actual_verdict == expected_verdict
        correct += int(passed)

        print("================================")
        print(f"Test {index}: {query}")
        print(f"Expected Verdict : {expected_verdict}")
        print(f"Actual Verdict   : {actual_verdict}")
        print(f"Final Status     : {result.get('status')}")
        print(f"Confidence       : {result.get('confidence')}")
        print(f"Result           : {'PASS' if passed else 'FAIL'}")

    accuracy = (correct / total) * 100 if total else 0

    print("\n========== SUMMARY ==========")
    print(f"Total Tests : {total}")
    print(f"Passed      : {correct}")
    print(f"Failed      : {total - correct}")
    print(f"Accuracy    : {accuracy:.2f}%")
    print("================================\n")


if __name__ == "__main__":
    run()
