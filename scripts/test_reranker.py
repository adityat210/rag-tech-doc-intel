from app.services.retriever import Retriever
from app.services.reranker import Reranker


def print_results(title, results):
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)

    for result in results:
        print()
        print("rank:", result["rank"])
        print("citation:", result["metadata"]["citation"])
        print("distance:", round(result["distance"],3))

        if "lexical_s" in result:
            print("lexical score:", round(result["lexical_s"], 3))
            print("vector score:", round(result["vector_s"], 3))
            print("cmbined score:", round(result["combined_s"], 3))

        print("preview:", result["chunk_text"][:250])
        print("-" * 80)


def main():
    query = "what is the main topic of the document?"

    retriever = Retriever()
    reranker = Reranker()

    baseline_results = retriever.retrieve(query=query, top_k=3)

    candidates = retriever.retrieve(query=query, top_k=6)
    reranked_results = reranker.rerank(query, candidates)[:3]

    print_results("baseline Retrieval", baseline_results)
    print_results("reranked Retrieval", reranked_results)


if __name__ == "__main__":
    main()