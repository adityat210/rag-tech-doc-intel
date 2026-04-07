import json

from app.config import PROCESSED_DATA_DIR, RAW_DATA_DIR
from app.services.ingest import ingest_directory

def main():
    #ingest documents, save to json file
    all_chunks = ingest_directory(RAW_DATA_DIR)
    output_file = PROCESSED_DATA_DIR / "ingested_chunks.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print("Ingested {0} chunks.".format(len(all_chunks)))
    print("Saved processed chunks to {0}".format(output_file))

if __name__ == "__main__":
    main()
