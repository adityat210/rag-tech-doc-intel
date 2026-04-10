from app.services.generator import Answers
from app.services.retriever import Retriever

def main():
    query = "what's the main topic of the document?"
    retriever = Retriever()
    retrieved_ = retriever.retrieve(query, top_k=3)

    generator = Answers()
    answer = generator.generate_(query, retrieved_)

    #print(retrieved_[0])

    print("\nQuestion:", query)
    print("\nAnswer: ", answer["answer"])

    print("\nCitations:")
    for citation in answer["citations"]:
        print("- ", citation)

if __name__ == "__main__":
    main()