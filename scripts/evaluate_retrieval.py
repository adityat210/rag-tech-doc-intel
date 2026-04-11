import json

from app.services.retriever import Retriever
from app.services.reranker import Reranker

def hit_at_k(results, expected_source, k):
    for result in results[:k]:
        #if found
        if result["metadata"]["source_file"] == expected_source:
            return 1
    return 0

def reciprocal_rank(results, expected_source):
    for idx, result in enumerate(results, start=1):
        if result["metadata"]["source_file"] == expected_source:
            return 1.0/(idx)
    return 0.0

def main():
    with open("app/data/eval/retrieval_eval.json", "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    #run baseline retrieval
    #run ranked retrieval
    #check if expected source in topk top 3 
    #compute hit@3 for both methods and compare
    retriever = Retriever()
    reranker = Reranker()
    baseline_hit1_total = 0
    baseline_hit3_total = 0
    baseline_mrr_total = 0.0

    reranked_hit1_total = 0
    reranked_hit3_total = 0
    reranked_mrr_total = 0.0

    total = len(eval_set)

    for item in eval_set:
        query = item["query"]
        expected_source = item["expected_source"]

        baseline_results = retriever.retrieve(query=query, top_k=3)

        candidate_results = retriever.retrieve(query=query, top_k=15 or 20)
        reranked_results = reranker.rerank(query, candidate_results)[:3]

        baseline_hit1 = hit_at_k(baseline_results, expected_source, 1)
        baseline_hit3 = hit_at_k(baseline_results, expected_source, 3)
        baseline_mrr = reciprocal_rank(baseline_results, expected_source)

        reranked_hit1 = hit_at_k(reranked_results, expected_source, 1)
        reranked_hit3 = hit_at_k(reranked_results, expected_source, 3)
        reranked_mrr = reciprocal_rank(reranked_results, expected_source)

        baseline_hit1_total += baseline_hit1
        baseline_hit3_total += baseline_hit3
        baseline_mrr_total += baseline_mrr

        reranked_hit1_total += reranked_hit1
        reranked_hit3_total += reranked_hit3
        reranked_mrr_total += reranked_mrr

        print()
        print("Query:", query)
        print("Expected source:", expected_source)
        print("Baseline hit@1:", baseline_hit1)
        print("Baseline hit@3:", baseline_hit3)
        print("Baseline MRR:", round(baseline_mrr, 4))
        print("Reranked hit@1:", reranked_hit1)
        print("Reranked hit@3:", reranked_hit3)
        print("Reranked MRR:", round(reranked_mrr, 4))

    print()
    print("=" * 60)
    print("Evaluation Summary")
    print("=" * 60)
    print("Total queries:", total)
    print("Baseline hit@1:", "{0:.2f}".format(baseline_hit1_total / total))
    print("Baseline hit@3:", "{0:.2f}".format(baseline_hit3_total / total))
    print("Baseline MRR:", "{0:.2f}".format(baseline_mrr_total / total))
    print("Reranked hit@1:", "{0:.2f}".format(reranked_hit1_total / total))
    print("Reranked hit@3:", "{0:.2f}".format(reranked_hit3_total / total))
    print("Reranked MRR:", "{0:.2f}".format(reranked_mrr_total / total))


if __name__ == "__main__":
    main()