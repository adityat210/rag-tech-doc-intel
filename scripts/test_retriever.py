from app.services.retriever import Retriever

def main():
    retriever = Retriever()
    q = "What is the main topic of the documnt?"
    results = retriever.retrieve(query=q, top_k=3)

    print("query:", q)
    print("results:", len(results))

    for res in results:
        print("\nrank:", res["rank"])
        print("distance:", res["distance"])
        print("citation:", res["metadata"]["citation"])
        print("text preview:", res["chunk_text"][:200])
        print("-" * 50)

if __name__ == "__main__":
    main()