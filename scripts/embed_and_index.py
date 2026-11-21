
import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


ROOT_DIR = Path(__file__).resolve().parents[1]

CHUNKS_FILE = (
    ROOT_DIR / "data" / "processed" / "pm-kisan-chunks.json"
)

CHROMA_DIR = ROOT_DIR / "chroma_db"

MODEL_NAME = "BAAI/bge-m3"
COLLECTION_NAME = "pm_kisan_mvp"

BATCH_SIZE = 16


def load_chunks():
    with open(CHUNKS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def prepare_metadata(chunk):
    return {
        "source_id": chunk["source_id"],
        "source_title": chunk["source_title"],
        "source_file": chunk["source_file"],
        "source_url": chunk["source_url"],
        "document_scope": chunk["document_scope"],
        "jurisdiction": chunk["jurisdiction"],
        "document_date": chunk["document_date"] or "",
        "document_reference_date": (
            chunk["document_reference_date"] or ""
        ),
        "publication_date": chunk["publication_date"] or "",
        "affected_clauses": ", ".join(chunk["affected_clauses"]),
        "content_status": chunk["content_status"],
        "page_start": chunk["page_start"],
        "page_end": chunk["page_end"]
    }


def main():
    chunks = load_chunks()

    print(f"Loaded {len(chunks)} chunks.")

    print(f"\nLoading embedding model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    client = chromadb.PersistentClient(
        path=str(CHROMA_DIR)
    )

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start:start + BATCH_SIZE]

        texts = [chunk["text"] for chunk in batch]
        ids = [chunk["chunk_id"] for chunk in batch]
        metadatas = [
            prepare_metadata(chunk) for chunk in batch
        ]

        embeddings = model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )

        collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings.tolist()
        )

        print(
            f"Indexed {min(start + len(batch), len(chunks))}"
            f"/{len(chunks)} chunks."
        )

    print("\nIndexing completed.")
    print("Collection:", COLLECTION_NAME)
    print("Stored chunks:", collection.count())
    print("Database:", CHROMA_DIR)


if __name__ == "__main__":
    main()
