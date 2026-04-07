import json 
from pathlib import Path
from typing import List

import faiss
import numpy as np

def build_faiss_index(embeddings: List[List[float]]):
    #builds a faiss index from the list of vector embeddings and saves it to disk at the specified path
    vectors = np.array(embeddings).astype("float32")
    
    if len(vectors.shape) != 2:
        raise ValueError("Embeddings must be a 2D array.")
    dimension = len(embeddings[0])
    index = faiss.IndexFlatL2(dimension)
    #simple exact nearest_neighbor search, euclidean distance
    index.add(vectors)

    return index

def save_index(index: faiss.IndexFlatL2, index_path: Path):
    #saves the faiss index to disk at the specified path, so don't need to recomput it every time
    faiss.write_index(index, str(index_path))

def load_index(index_path: Path):
    #loads a faiss index from disk at the specified path and returns it
    index = faiss.read_index(str(index_path))
    return index

def save_metadata(metadata: List[dict], metadata_path: Path):
    #saves chunk metadata to disk as JSON, as matching position to vector 
    #metadata position 0 -> vector at position 0, so can retrieve text chunk and other info when get vector matches back from faiss index search
    with metadata_path.open("w", encoding="utf-8") as output_file:
        json.dump(metadata, output_file, indent=2, ensure_ascii=False)

def load_metadata(metadata_path: Path):
    #loads chunk metadata from disk, vector at position 0 -> metadata at position 0
    with metadata_path.open("r", encoding="utf-8") as input_file:
        return json.load(input_file)