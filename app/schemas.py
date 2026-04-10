from typing import List
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class RetrivedChunk(BaseModel):
    rank: int
    chunk_text: str
    citation: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[str]
    retrieved_: List[RetrivedChunk]