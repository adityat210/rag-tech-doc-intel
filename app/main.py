from fastapi import FastAPI

from app.schemas import QueryRequest, RetrievedChunk, QueryResponse
from app.services.generator import Answers
from app.services.retriever import Retriever

app = FastAPI(
    title = "Domain-Specific RAG system for technical doc intelligence",
    version = "0.1.0",
)

retriever = Retriever()
generator = Answers()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query_docuuments(request: QueryRequest):
    retrieved_ = retriever.retrieve(request.query, top_k = request.top_k)
    answer = generator.generate_(request.query, retrieved_)

    retrieved_chunks = []
    for chunk in retrieved_:
        retrieved_chunks.append(
            RetrievedChunk(
                rank = chunk["rank"],
                chunk_text = chunk["chunk_text"][:300],
                citation = chunk["metadata"]["citation"],
            )
        )
    
    return QueryResponse(
        answer = answer["answer"],
        citations = answer["citations"],
        retrieved_ = retrieved_chunks,
    )