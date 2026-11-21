
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

INPUT_DIR = ROOT_DIR / "data" / "processed" / "pm-kisan"
OUTPUT_FILE = ROOT_DIR / "data" / "processed" / "pm-kisan-chunks.json"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200


def split_text(text):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def process_document(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        document = json.load(file)

    source = document["source_metadata"]
    chunks = []

    for page in document["pages"]:
        page_number = page["page_number"]
        text = page["cleaned_text"].strip()

        if not text:
            continue

        page_chunks = split_text(text)

        for index, chunk_text in enumerate(page_chunks, start=1):
            chunk_id = (
                f"source_{document['source_id']}"
                f"_page_{page_number}"
                f"_chunk_{index}"
            )

            chunks.append({
                "chunk_id": chunk_id,
                "source_id": document["source_id"],
                "source_title": source["title"],
                "source_file": document["source_file"],
                "source_url": source["source_url"],
                "document_scope": document["document_scope"],
                "jurisdiction": document["jurisdiction"],
                "document_date": source["document_date"],
                "document_reference_date": source["document_reference_date"],
                "publication_date": source["publication_date"],
                "affected_clauses": source["affected_clauses"],
                "content_status": source["metadata_status"],
                "page_start": page_number,
                "page_end": page_number,
                "text": chunk_text
            })

    return chunks


def main():
    all_chunks = []

    input_files = sorted(INPUT_DIR.glob("*.json"))

    for file_path in input_files:
        document_chunks = process_document(file_path)
        all_chunks.extend(document_chunks)

        print(
            f"{file_path.name}: "
            f"{len(document_chunks)} chunks"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            all_chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nChunking completed.")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
