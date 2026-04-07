import json
from app.config import INDEX_DIR, PROCESSED_DATA_DIR
from app.services.embedder import Embedder
from app.services.vector_store import build_faiss_index, save_index, save_metadata

def main():
    input_path = PROCESSED_DATA_DIR / "ingested_chunks.json"

    with input_path.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    print("loaded {0} chunks.".format(len(chunks)))

    
    

    texts = [chunk["text"] for chunk in chunks]
    metadata = [chunk["metadata"] for chunk in chunks]

    embed = Embedder()
    embeddings = embed.embed_texts(texts)

    index = build_faiss_index(embeddings)

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    save_index(index, INDEX_DIR / "faiss.index")
    save_metadata(metadata, INDEX_DIR / "metadata.json")

    with (INDEX_DIR / "chunk_texts.json").open("w", encoding="utf-8") as f:
        json.dump(texts, f, indent=2, ensure_ascii=False)

    print("saving faiss index to {0}".format(INDEX_DIR / "faiss.index"))
    print("saving metadata to {0}".format(INDEX_DIR / "metadata.json"))
    print("saving chunk texts to {0}".format(INDEX_DIR / "chunk_texts.json"))

if __name__ == "__main__":
    main()

