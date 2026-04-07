from pathlib import Path
from typing import Dict

def build_chunk_metadata(source_file: Path, page_number: int, chunk_index: int, total_chunks_on_page: int):
    #bulds metadata for chunk of document text, keeping seperate from parsing and chunking
    return {
        "source_file": source_file.name,
        "page_numnber": page_number,
        "chunk_index": chunk_index,
        "total_chunks_on_page": total_chunks_on_page,
        "source_type": source_file.suffix.lower().replace(".", ""),
        "citation": "{0} - page {1}".format(source_file.name, page_number)
    }