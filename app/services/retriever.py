import json 
from typing import List, Dict

import numpy as np

from app.config import INDEX_DIR
from app.services.embedder import Embedder
from app.services.vector_store import load_index, load_metadata

class Retriever:
    #load retrieval and return top-k matching chunks for a query
    def __init__(self):
        self.index = load_index(INDEX_DIR / "faiss.index")
        self.metadata = load_metadata(INDEX_DIR / "metadata.json")
        self.embed = Embedder()

        with (INDEX_DIR/ "chunk_texts.json").open("r", encoding="utf-8") as f:
            self.chunk_texts = json.load(f)
    
    def retrieve(self, query:str, top_k:int=3):
        #retrieve most relevant chunks for given user query
        query_embed = self.embed.embed_texts([query])[0]
        query_vector = np.array([query_embed]).astype("float32")

        distances, indices = self.index.search(query_vector, top_k)

        result = []
        for rank, chunk_index in enumerate(indices[0]):
            if chunk_index == -1:
                continue

            result.append(
                {
                    "rank": rank + 1,
                    "chunk_index": int(chunk_index),
                    "distance": float(distances[0][rank]),
                    "chunk_text": self.chunk_texts[chunk_index],
                    "metadata": self.metadata[chunk_index]
                }
            )

        return result



