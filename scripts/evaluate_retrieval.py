import json

from app.services.retriever import Retriever
from app.services.reranker import Reranker

def hit_at_k(results, expected_source):
    for result in results:
        #if found
        if result["metadata"]["source_file"] == expected_source:
            return 1
    return 0

def main():
    with open("app/data/eval/retrieval_eval.json", "r", encoding="utf-8") as f:
        eval_set = json.load(f)

    #run baseline retrieval
    #run ranked retrieval
    #check if expected source in topk top 3 
    #compute hit@3 for both methods and compare
    retriever = Retriever()
    reranker = Reranker()

    baseline_hits = 0
    reranked_hits = 0
    total = len(eval_set)

    for item in eval_set:
        query = item["query"]
        expected_source = item["expected_source"]

        baseline_results = retriever.retrieve(query=query, top_k=3)

        candidate_results = retriever.retrieve(query=query, top_k = 6)
        reranked_results = reranker.rerank(query, candidate_results)[:3]

        baseline_hit = hit_at_k(baseline_results, expected_source)
        reranked_hit = hit_at_k(reranked_results, expected_source)

        baseline_hits += baseline_hit
        reranked_hits += reranked_hit

        print()
        print("Query:", query)
        print("expected source:", expected_source)
        print("baseline hit@3:", baseline_hit)
        print("reranked hit@3:", reranked_hit)

    print()
    print("=" * 60)
    print("evaluation summary")
    print("=" * 60)
    print(f"total Queries: {total}")
    print("baseline hit", "{0:.2f}".format(baseline_hits/total))
    print("reranked hit", "{0:.2f}".format(reranked_hits/total))

if __name__ == "__main__":
    main()


