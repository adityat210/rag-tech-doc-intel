import json

from app.config import INDEX_DIR, PROCESSED_DATA_DIR
from app.services.embedder import Embedder
from app.services.vector_store import build_faiss_index, save_index, save_metadata


def main():
    input_path = PROCESSED_DATA_DIR / "ingested_chunks.json"

    with input_path.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    sample_chunks = chunks[:5]
    texts = [chunk["text"] for chunk in sample_chunks]
    metadata = [chunk["metadata"] for chunk in sample_chunks]

    embedder = Embedder()
    embeddings = embedder.embed_texts(texts)

    index = build_faiss_index(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    save_index(index, INDEX_DIR / "test_faiss.index")
    save_metadata(metadata, INDEX_DIR / "test_metadata.json")

    print("built test index with {0} vectors.".format(index.ntotal))
    print("saved test index & metadata to app/data/index/")


if __name__ == "__main__":
    main()