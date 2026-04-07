import json

from app.config import PROCESSED_DATA_DIR
from app.services.embedder import Embedder


def main():
    input_path = PROCESSED_DATA_DIR / "ingested_chunks.json"

    with input_path.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    texts = [chunk["text"] for chunk in chunks[:3]]

    embedder = Embedder()
    embeddings = embedder.embed_texts(texts)

    print("embedded {0} chunks.".format(len(embeddings)))
    print("embedding dimension:", len(embeddings[0]))
    print("first 5 values of embedding:", embeddings[0][:5])


if __name__ == "__main__":
    main()