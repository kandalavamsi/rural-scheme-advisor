from pathlib import Path
import pymupdf

pdf_path=Path("data/raw/pm-kisan/revised-operational-guidelines-2020.pdf")

if not pdf_path.exists():
    raise FileNotFoundError(f"PDF not found: {pdf_path}")

with pymupdf.open(pdf_path) as document:
     print("Total pages:", len(document))
     print("Metadata:", document.metadata)

     for page_number, page in enumerate(document[:3], start=1):
        text = page.get_text("text")

        print(f"\n{'=' * 50}")
        print(f"PAGE {page_number}")
        print(f"{'=' * 50}")
        print(text[:2000])