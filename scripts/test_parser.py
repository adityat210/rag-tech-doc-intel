from pathlib import Path

from app.services.parser import parse_document


def main() -> None:
    raw_dir = Path("app/data/raw")

    for file_path in sorted(raw_dir.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in {".pdf", ".txt"}:
            print("\nParsing:", file_path.name)
            pages = parse_document(file_path)
            print("Pages parsed:", len(pages))

            if pages:
                preview = pages[0]["text"][:300]
                print("First page preview:")
                print(preview)
                print("-" * 60)


if __name__ == "__main__":
    main()