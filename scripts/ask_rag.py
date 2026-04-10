import argparse

from app.services.generator import Answers
from app.services.retriever import Retriever

def main():
    parser = argparse.ArgumentParser(description="ask questions against the RAG document system.")
    parser.add_argument("query", type=str, help="question to ask the system")
    parser.add_argument("--top_k", type=int, default=3, help="number of retrieved chunks using for answer generation")

    args = parser.parse_args()

    retriever = Retriever()
    retrieved_ = retriever.retrieve(args.query, top_k = args.top_k)

    generator = Answers()
    result = generator.generate_(args.query, retrieved_)

    print()
    print("Question:", args.query)
    print()
    print("Answer: ", result["answer"])

    print()
    print("Citations:")
    for citation in result["citations"]:
        print("- ", citation)
    
    print()
    print("retrieved context preview:")
    for chunk in retrieved_:
        print()
        print("[", chunk["metadata"]["citation"], "]")
        print("- ", chunk["chunk_text"][:100], "...")
        print("-" * 50)

if __name__ == "__main__":
    main()
