import re
from typing import Dict, List

class Reranker:
    #reranking that combines overlap with vector retrieval results
    def tokenizing(self, text: str):
        stopwords = {
            "the", "a", "an", "what", "does", "how", "is", "are", "of", "and",
            "in", "to", "it", "this", "that", "paper", "document", "essay", "main"
        }
        token = re.findall(r"\b\w+\b", text.lower())
        return {t for t in token if t not in stopwords}
    
    def lexical_overlap_score(self, query: str, chunk_text: str):
        #score chunk by fraction of unique tokens that appear in the chunk
        query_ = set(self.tokenizing(query))
        chunk_ = set(self.tokenizing(chunk_text))

        #base case, avoid division by 0
        if not query_:
            return 0.0
        
        #overlap = query_.intersection(chunk_)
        #return len(overlap) / len(query_)
        overlap = query_.intersection(chunk_)

        # weight longer / more informative tokens higher
        score = 0.0
        for token in overlap:
            score += len(token)

        return score / (sum(len(t) for t in query_) + 1e-8)
    
    def rerank(self, query: str, retrieved_chunks: List[Dict[str, object]]):
        #rerank retrieved chunks, combining overlap and vector similarity
        rerank = []
        for chunk in retrieved_chunks:
            #how many query words appear in the chunk
            lexical_s = self.lexical_overlap_score(query, chunk["chunk_text"])

            vector_d = chunk["distance"]
            #faiss result gives distance, higher is better
            vector_s = 1.0/(1.0 + vector_d)

            #create updated chunk dict with new scores, combined is weighted average of the two
            combined_s = 0.6 * vector_s + 0.4 * lexical_s
            updated_ = dict(chunk)
            updated_["lexical_s"] = lexical_s
            updated_["vector_s"] = vector_s
            updated_["combined_s"] = combined_s

            rerank.append(updated_)

        #sort by combined score, highest first
        rerank.sort(key=lambda x: x["combined_s"], reverse=True)

        for rank, chunk in enumerate(rerank):
            chunk["rank"] = rank + 1

        return rerank


