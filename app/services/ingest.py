from pathlib import Path
from typing import Dict, List

from app.config import CHUNK_OVERLAP, CHUNK_SIZE, SUPPORTED_EXTENSIONS
from app.services.chunker import chunk_text
from app.services.metadata import build_chunk_metadata
from app.services.parser import parse_document

def ingest_document(file_path: Path):
    #parse doc, split into chunks, build and attach metadata
    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return []
    
    parsed_pages = parse_document(file_path)
    all_chunks = []

    for page in parsed_pages:
        page_number = page["page_number"]
        page_text = page["text"]

        chunks = chunk_text(page_text, CHUNK_SIZE, CHUNK_OVERLAP)

        for index, chunk in enumerate(chunks):
            metadata = build_chunk_metadata(file_path, page_number, index, len(chunks))
            all_chunks.append({
                "text": chunk,
                "metadata": metadata
            })
    
    return all_chunks

def ingest_directory(raw_data_dir: Path):
    #ingest all supported documents in a directory
    #for each file: parse into page-level text, chunk each page, attach metadata, return one flat list of chunk records
    all_chunks = []

    for file_path in sorted(raw_data_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            chunks = ingest_document(file_path)
            all_chunks.extend(chunks)

    return all_chunks