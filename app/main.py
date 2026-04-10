from fastapi import FastAPI

import time
from app.utils.logging_utils import log_query_event

from app.schemas import QueryRequest, RetrievedChunk, QueryResponse
from app.services.generator import Answers
from app.services.retriever import Retriever

app = FastAPI(
    title = "RAG System for Technical Document Intelligence",
    version = "0.1.0",
)

retriever = Retriever()
generator = Answers()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def query_docuuments(request: QueryRequest):
    start = time.time()

    retrieved_ = retriever.retrieve(request.query, top_k = request.top_k)
    answer = generator.generate_(request.query, retrieved_)

    #measures time for retrieval + generation + response assembly
    latency_seconds = round(time.time() - start, 3)

    #need to write log entry
    log_query_event(
        {
            "query": request.query,
            "top_k": request.top_k,
            "retrieved_count": len(retrieved_),
            "citations": answer["citations"],
            "latency_seconds": latency_seconds,
        }
    )

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