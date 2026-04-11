from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
INDEX_DIR = DATA_DIR / "index"

CHUNK_SIZE = 300
CHUNK_OVERLAP = 80
SUPPORTED_EXTENSIONS = {".pdf", ".txt"}