# RAG Based Document Question Answering
Retrieval-Augmented Generation (RAG) system for querying and analyzing document collections using embedding-based retrieval and reranking.
After ingesting docs and building the index, you can query the indexed chunks from the command line

## Overview
Project implements RAG end-to-end, allows users to ask natural language questies over a collection of documents (PDF and .txt)

1. Ingests and parses raw docs
2. Chunks and embeds contents based on sizing in config
3. Indexes embeddings using FAISS
4. Retrieves the relevant chunks for a query
5. Reranks results using an optimized hybrid lexical + semantic socring approach
6. Generates grounded answers with citations

## Results
Evaluation was performed on collection of 1,900 document chunks across multiple docs
### Baseline Retrieval
- hit@1: 0.67
- hit@3: 0.90
- MRR: 0.78

### + W/ Hybrid Reranking
- hit@1: 0.86
- hit@3: 1.00
- MRR: 0.92

### Latency Stats
- Avg latency: 1.9738 seconds
- Median latency: 1.4455 seconds
