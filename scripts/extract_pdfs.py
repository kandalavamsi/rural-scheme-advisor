
from pathlib import Path
import json
import pymupdf

INPUT_DIR = Path("data/raw/pm-kisan")
OUTPUT_DIR = Path("data/processed/pm-kisan")
MANIFEST_PATH = Path("data/sources/pm-kisan-sources.json")


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u00a0", " ")

    lines = text.split("\n")

    cleaned_lines = []
    previous_line_was_blank = False

    for line in lines:
        line = line.strip()

        if not line:
            if not previous_line_was_blank:
                cleaned_lines.append("")

            previous_line_was_blank = True

        else:
            cleaned_lines.append(line)
            previous_line_was_blank = False

    return "\n".join(cleaned_lines).strip()


def load_source_manifest():
    with MANIFEST_PATH.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    sources = manifest.get("sources", [])

    source_map = {}

    for source in sources:
        relative_path = source["local_relative_path"]

        if relative_path in source_map:
            raise ValueError(
                f"Duplicate manifest path: {relative_path}"
            )

        source_map[relative_path] = source

    return source_map


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    source_map = load_source_manifest()

    pdf_files = sorted(INPUT_DIR.rglob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF files found in the input directory."
        )

    processed_paths = set()

    for pdf_path in pdf_files:
        print(f"\nProcessing: {pdf_path.name}")

        try:
            relative_path = pdf_path.relative_to(INPUT_DIR).as_posix()

            if relative_path not in source_map:
                raise ValueError(
                    f"PDF is missing from source manifest: {relative_path}"
                )

            source_metadata = source_map[relative_path]
            processed_paths.add(relative_path)

            with pymupdf.open(pdf_path) as document:
                pages = []

                for page_number, page in enumerate(document, start=1):
                    raw_text = page.get_text("text")
                    cleaned_text = clean_text(raw_text)

                    pages.append({
                        "page_number": page_number,
                        "raw_text": raw_text,
                        "cleaned_text": cleaned_text
                    })

                extracted_data = {
                    "source_id": source_metadata["source_id"],
                    "source_file": pdf_path.name,
                    "source_relative_path": relative_path,
                    "source_metadata": source_metadata,
                    "document_scope": source_metadata["document_scope"],
                    "jurisdiction": source_metadata["jurisdiction"],
                    "total_pages": len(document),
                    "pdf_metadata": document.metadata,
                    "pages": pages
                }

            output_filename = pdf_path.stem + ".json"
            output_path = OUTPUT_DIR / output_filename

            with output_path.open("w", encoding="utf-8") as file:
                json.dump(
                    extracted_data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            total_characters = sum(
                len(page["cleaned_text"]) for page in pages
            )

            print("Source ID:", source_metadata["source_id"])
            print("Scope:", source_metadata["document_scope"])
            print("Jurisdiction:", source_metadata["jurisdiction"])
            print("Pages extracted:", len(pages))
            print("Cleaned characters:", total_characters)
            print("JSON saved:", output_path)

        except Exception as error:
            print(f"FAILED: {pdf_path.name}")
            print("Reason:", error)
            raise

    unprocessed_sources = set(source_map) - processed_paths

    if unprocessed_sources:
        raise ValueError(
            f"Manifest entries without matching PDFs: {unprocessed_sources}"
        )


if __name__ == "__main__":
    main()
