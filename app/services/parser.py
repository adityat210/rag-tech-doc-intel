from pathlib import Path
from typing import Dict, List

from pypdf import PdfReader


def clean_text(text: str) -> str:
    """
    Normalize extracted text by removing excess whitespace and blank lines.
    """
    if not text:
        return ""

    text = text.replace("\xa0", " ")
    lines = [line.strip() for line in text.splitlines()]
    lines = [line for line in lines if line]

    return " ".join(lines)


def parse_pdf(file_path: Path) -> List[Dict[str, object]]:
    """
    Extract cleaned text from each page of a PDF.
    Returns a list of page-level records.
    """
    pages = []
    reader = PdfReader(str(file_path))

    for page_index, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            pages.append(
                {
                    "page_number": page_index + 1,
                    "text": cleaned_text,
                }
            )

    return pages


def parse_txt(file_path: Path) -> List[Dict[str, object]]:
    """
    Read a plain text file and return it as a single page-style record.
    """
    raw_text = file_path.read_text(encoding="utf-8", errors="ignore")
    cleaned_text = clean_text(raw_text)

    if not cleaned_text:
        return []

    return [
        {
            "page_number": 1,
            "text": cleaned_text,
        }
    ]


def parse_document(file_path: Path) -> List[Dict[str, object]]:
    """
    Parse a supported document type into page-level text records.
    """
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        return parse_pdf(file_path)

    if suffix == ".txt":
        return parse_txt(file_path)

    raise ValueError("Unsupported file type: {0}".format(suffix))