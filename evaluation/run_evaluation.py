"""
Role in simple language: “Is the system correct across many queries?”

Example test case:

{
    "query": "What is the refund period?",
    "expected_status": "SAFE",
    "expected_source_contains": "billing_and_refund_policy_v2"
}

Evaluation runs 20 such queries and outputs:
    • Status accuracy: 95%
    • Retrieval Recall@5: 90%
    • Refusal precision: 100%

If you ever:
    • Change retrieval
    • Add hybrid search
    • Switch embedding model
    • Tune governance prompts

Evaluation tells you:
Did it improve or did it break?

THIS IS ONLY USED FOR OFFLINE CASE AND NOT USED IN REALTIME DECISION MAKING.
Evaluation exists for one reason:

To know if your system is actually good — instead of just feeling good about it.
"""

import json
from src.pipeline.rag_pipeline import RAGPipeline
from evaluation.metrics import evaluate_retrieval


def run():
    pipeline = RAGPipeline()

    with open("evaluation/test_cases.json", "r") as f:
        test_cases = json.load(f)

    # # -------------------------
    # # Retrieval Eval
    # # -------------------------
    # print("\n========== RETRIEVAL EVALUATION ==========\n")

    # retrieval_results = evaluate_retrieval(
    #     test_cases=test_cases,
    #     top_k=5,
    #     deduplicate_documents=True   # <-- Added flag for eval-only dedupe
    # )

    # print(f"Total Queries (retrieval evaluated): {retrieval_results['total_queries']}")
    # print(f"Recall@5: {retrieval_results['recall@5']}")
    # print(f"MRR: {retrieval_results['mrr']}")

    # # Optional visibility (safe, eval-only insight)
    # if "avg_unique_docs_in_top_k" in retrieval_results:
    #     print(f"Avg Unique Docs in Top@5: {retrieval_results['avg_unique_docs_in_top_k']}")

    # print("\n===========================================\n")

    # -------------------------
    # End-to-End Eval
    # -------------------------

    total = len(test_cases)
    correct = 0

    print("========== END-TO-END EVALUATION ==========\n")

    for i, case in enumerate(test_cases, 1):
        query = case["query"]
        expected_verdict = case["expected_verdict"]

        result = pipeline.run(query)

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

### evaluation checker -> python -m evaluation.run_evaluation

"""
Result:
Total Queries (retrieval evaluated): 18
Recall@5: 0.8889
MRR: 0.5259

Recall - In 89% of cases, the correct document appeared in the top 5. Hybrid retrieval might slightly improve recall.

MRR - On average, the correct document was ranked around 2nd or 3rd position. 

	If MRR = 1.0
	Correct doc always at rank 1.
			If MRR = 0.5
			Correct doc is often around rank 2.
0.5259 suggests: On average, the correct document appears around position 2. But this is where reranking can help.

"""

