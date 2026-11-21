
from pathlib import Path
import pymupdf

pdf_directory = Path("data/raw/pm-kisan")

for pdf_path in sorted(pdf_directory.rglob("*.pdf")):
    print(f"\n{'=' * 65}")
    print("FILE:", pdf_path.name)
    print("=" * 65)

    try:
        with pymupdf.open(pdf_path) as document:
            total_pages = len(document)
            total_characters = 0
            empty_pages = 0

            for page in document:
                text = page.get_text("text").strip()
                total_characters += len(text)

                if not text:
                    empty_pages += 1

            print("Total pages:", total_pages)
            print("Total extracted characters:", total_characters)
            print("Pages without extractable text:", empty_pages)

    except Exception as error:
        print("ERROR:", error)
