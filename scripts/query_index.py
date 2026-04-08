import argparse

from app.services.retriever import Retriever

def main():
    parser = argparse.ArgumentParser(description="query the indexed doc chunks using vector search through similarity")
    #lets pass arguments from the terminal, can run different queries directly
    parser.add_argument("--query", type=str, help="query to search for")
    parser.add_argument("--top_k", type=int, default=3, help="# of top matching chunks to return")

    args = parser.parse_args()
    retriever = Retriever()
    result = retriever.retrieve(query=args.query, top_k=args.top_k)

    print("\nquery:", (args.query))
    print("top-k:", (args.top_k))
    print("results: ",(len(result)))

    for res in result:
        print("\nrank:", res["rank"])
        print("distance:", res["distance"])
        print("citation:", res["metadata"]["citation"])
        print("text preview:", res["chunk_text"][:400])
        print("-" * 50)

if __name__ == "__main__":
    main()